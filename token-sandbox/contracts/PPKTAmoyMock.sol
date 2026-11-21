// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Pausable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @notice TESTNET ONLY: PPKT simulator; tokens have no backing, cash value or redemption claim.
 * @dev This contract does NOT attest to fiat custody, issuer solvency or bank payment.
 * Do not deploy this test artifact to any mainnet; deployment is deliberately chain-restricted.
 */
contract PPKTAmoyMock is ERC20, ERC20Pausable, AccessControl {
    bytes32 public constant ATTESTER_ROLE = keccak256("ATTESTER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant REDEEMER_ROLE = keccak256("REDEEMER_ROLE");
    bytes32 public constant SETTLEMENT_ROLE = keccak256("SETTLEMENT_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    uint256 public immutable outstandingSupplyCeiling;
    uint256 public immutable singleMintCeiling;

    struct MintApproval {
        address recipient;
        uint256 amount;
        address attester;
        bool exists;
        bool executed;
    }

    // 0 = absent; 1 = tokens held; 2 = burned but PHP payable UNSETTLED;
    // 3 = fiat settlement reported by a SIMULATOR ONLY; 4 = refunded from escrow
    struct Redemption {
        address holder;
        uint256 amount;
        uint8 state;
        bytes32 simulatedFiatEvidence;
    }

    mapping(bytes32 => MintApproval) public mintApprovals;
    mapping(bytes32 => Redemption) public redemptions;

    event FakeFundingAttested(bytes32 indexed fundingRef, address indexed recipient, uint256 amount, address attester);
    event SimulatedMintExecuted(bytes32 indexed fundingRef, address indexed recipient, uint256 amount);
    event RedemptionLocked(bytes32 indexed redemptionRef, address indexed holder, uint256 amount);
    event RedemptionBurnedPayablePending(bytes32 indexed redemptionRef, address indexed holder, uint256 amount);
    event SimulatedFiatSettlementReported(bytes32 indexed redemptionRef, bytes32 simulatedEvidence);
    event RedemptionEscrowRefunded(bytes32 indexed redemptionRef, address indexed holder, uint256 amount);

    constructor(address admin, uint256 supplyCeiling, uint256 mintCeiling)
        ERC20("PPKT AMOY TEST - NO VALUE", "tPPKT")
    {
        require(block.chainid == 80002 || block.chainid == 31337, "TEST_NETWORK_ONLY");
        require(admin != address(0), "ZERO_ADMIN");
        require(mintCeiling > 0 && supplyCeiling >= mintCeiling, "BAD_LIMITS");
        outstandingSupplyCeiling = supplyCeiling;
        singleMintCeiling = mintCeiling;
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
    }

    function decimals() public pure override returns (uint8) { return 6; }

    function attestFakeFunding(bytes32 ref, address recipient, uint256 amount)
        external onlyRole(ATTESTER_ROLE) whenNotPaused
    {
        require(ref != bytes32(0), "ZERO_REFERENCE");
        require(!mintApprovals[ref].exists, "MINT_REFERENCE_USED");
        require(recipient != address(0), "ZERO_RECIPIENT");
        require(amount > 0 && amount <= singleMintCeiling, "MINT_LIMIT");
        mintApprovals[ref] = MintApproval(recipient, amount, msg.sender, true, false);
        emit FakeFundingAttested(ref, recipient, amount, msg.sender);
    }

    function executeSimulatedMint(bytes32 ref)
        external onlyRole(MINTER_ROLE) whenNotPaused
    {
        MintApproval storage a = mintApprovals[ref];
        require(a.exists && !a.executed, "NO_PENDING_MINT");
        require(a.attester != msg.sender, "INDEPENDENT_OPERATOR_REQUIRED");
        require(totalSupply() + a.amount <= outstandingSupplyCeiling, "SUPPLY_CEILING");
        a.executed = true; // set before external-facing token event
        _mint(a.recipient, a.amount);
        emit SimulatedMintExecuted(ref, a.recipient, a.amount);
    }

    function lockForSimulatedRedemption(bytes32 ref, uint256 amount)
        external whenNotPaused
    {
        require(ref != bytes32(0) && redemptions[ref].state == 0, "REDEMPTION_REFERENCE_USED");
        require(amount > 0, "ZERO_AMOUNT");
        redemptions[ref] = Redemption(msg.sender, amount, 1, bytes32(0));
        _transfer(msg.sender, address(this), amount);
        emit RedemptionLocked(ref, msg.sender, amount);
    }

    function burnPendingSimulatedPayout(bytes32 ref)
        external onlyRole(REDEEMER_ROLE) whenNotPaused
    {
        Redemption storage r = redemptions[ref];
        require(r.state == 1, "NOT_LOCKED");
        r.state = 2;
        _burn(address(this), r.amount);
        // On-chain burn DOES NOT extinguish the outstanding off-chain PHP payable.
        emit RedemptionBurnedPayablePending(ref, r.holder, r.amount);
    }

    function refundEscrowBeforeBurn(bytes32 ref)
        external onlyRole(REDEEMER_ROLE) whenNotPaused
    {
        Redemption storage r = redemptions[ref];
        require(r.state == 1, "NOT_REFUNDABLE");
        r.state = 4;
        _transfer(address(this), r.holder, r.amount);
        emit RedemptionEscrowRefunded(ref, r.holder, r.amount);
    }

    function recordSimulatedFiatSettlement(bytes32 ref, bytes32 evidenceHash)
        external onlyRole(SETTLEMENT_ROLE) whenNotPaused
    {
        Redemption storage r = redemptions[ref];
        require(r.state == 2, "NOT_BURNED_PENDING");
        require(evidenceHash != bytes32(0), "EMPTY_SIM_EVIDENCE");
        r.state = 3;
        r.simulatedFiatEvidence = evidenceHash;
        emit SimulatedFiatSettlementReported(ref, evidenceHash);
    }

    function pause() external onlyRole(PAUSER_ROLE) { _pause(); }
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) { _unpause(); }

    function _update(address from, address to, uint256 value)
        internal override(ERC20, ERC20Pausable)
    {
        super._update(from, to, value);
    }
}
