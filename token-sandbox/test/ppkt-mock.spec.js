const { expect } = require("chai");
const { ethers } = require("hardhat");
const UNIT = 1_000_000n;

async function mustRevert(action) {
  let failed = false;
  try {
    const maybeTx = await action;
    if (maybeTx && typeof maybeTx.wait === "function") await maybeTx.wait();
  } catch (_) { failed = true; }
  expect(failed, "transaction must revert").to.equal(true);
}

describe("PPKT Amoy sandbox mock (NO VALUE)", function () {
  let token, admin, attester, minter, redeemer, reporter, user, other;
  let mintRef, redeemRef;
  beforeEach(async function () {
    [admin, attester, minter, redeemer, reporter, user, other] = await ethers.getSigners();
    const factory = await ethers.getContractFactory("PPKTAmoyMock");
    token = await factory.deploy(admin.address, 1_000n * UNIT, 200n * UNIT);
    await token.waitForDeployment();
    await token.grantRole(await token.ATTESTER_ROLE(), attester.address);
    await token.grantRole(await token.MINTER_ROLE(), minter.address);
    await token.grantRole(await token.REDEEMER_ROLE(), redeemer.address);
    await token.grantRole(await token.SETTLEMENT_ROLE(), reporter.address);
    await token.grantRole(await token.PAUSER_ROLE(), admin.address);
    mintRef = ethers.id("synthetic-bank-confirmation-0001");
    redeemRef = ethers.id("synthetic-redemption-0001");
  });

  async function seed(amount = 100n * UNIT) {
    await token.connect(attester).attestFakeFunding(mintRef, user.address, amount);
    await token.connect(minter).executeSimulatedMint(mintRef);
  }

  it("starts with zero supply, is named as an unmistakable mock", async () => {
    expect(await token.totalSupply()).to.equal(0n);
    expect(await token.decimals()).to.equal(6n);
    expect(await token.symbol()).to.equal("tPPKT");
    expect((await token.name()).includes("NO VALUE")).to.equal(true);
  });

  it("permits only attested, independently executed minting", async () => {
    await mustRevert(token.connect(other).attestFakeFunding(mintRef, user.address, 10n * UNIT));
    await mustRevert(token.connect(minter).executeSimulatedMint(mintRef));
    await seed();
    expect(await token.balanceOf(user.address)).to.equal(100n * UNIT);
    await mustRevert(token.connect(minter).executeSimulatedMint(mintRef));
    await mustRevert(token.connect(attester).attestFakeFunding(mintRef, other.address, UNIT));
  });

  it("forbids attester executing their own approval even with both roles", async () => {
    await token.grantRole(await token.MINTER_ROLE(), attester.address);
    await token.connect(attester).attestFakeFunding(mintRef, user.address, UNIT);
    await mustRevert(token.connect(attester).executeSimulatedMint(mintRef));
  });

  it("enforces single-mint and outstanding-supply ceilings", async () => {
    await mustRevert(token.connect(attester).attestFakeFunding(mintRef, user.address, 201n * UNIT));
    await token.connect(attester).attestFakeFunding(mintRef, user.address, 200n * UNIT);
    await token.connect(minter).executeSimulatedMint(mintRef);
    expect(await token.totalSupply()).to.equal(200n * UNIT);
  });

  it("locks, burns, and preserves a payable until simulated fiat evidence", async () => {
    await seed();
    await token.connect(user).lockForSimulatedRedemption(redeemRef, 20n * UNIT);
    let r = await token.redemptions(redeemRef);
    expect(r.state).to.equal(1n);
    await mustRevert(token.connect(other).burnPendingSimulatedPayout(redeemRef));
    await token.connect(redeemer).burnPendingSimulatedPayout(redeemRef);
    r = await token.redemptions(redeemRef);
    expect(r.state).to.equal(2n);
    expect(await token.totalSupply()).to.equal(80n * UNIT);
    await mustRevert(token.connect(redeemer).burnPendingSimulatedPayout(redeemRef));
    await token.connect(reporter).recordSimulatedFiatSettlement(redeemRef, ethers.id("fake-provider-receipt"));
    r = await token.redemptions(redeemRef);
    expect(r.state).to.equal(3n);
    await mustRevert(token.connect(reporter).recordSimulatedFiatSettlement(redeemRef, ethers.id("repeat")));
  });

  it("refunds only escrowed, not burned redemption", async () => {
    await seed();
    await token.connect(user).lockForSimulatedRedemption(redeemRef, 20n * UNIT);
    await token.connect(redeemer).refundEscrowBeforeBurn(redeemRef);
    expect(await token.balanceOf(user.address)).to.equal(100n * UNIT);
    await mustRevert(token.connect(redeemer).burnPendingSimulatedPayout(redeemRef));
  });

  it("pauses transfers and independent mint/redemption operations", async () => {
    await seed();
    await token.pause();
    await mustRevert(token.connect(user).transfer(other.address, UNIT));
    await mustRevert(token.connect(user).lockForSimulatedRedemption(redeemRef, UNIT));
    await mustRevert(token.connect(attester).attestFakeFunding(ethers.id("next"), user.address, UNIT));
    await token.unpause();
    await token.connect(user).transfer(other.address, UNIT);
    expect(await token.balanceOf(other.address)).to.equal(UNIT);
  });

  it("rejects fake evidence and invalid duplicate redemption ids", async () => {
    await seed();
    await token.connect(user).lockForSimulatedRedemption(redeemRef, UNIT);
    await mustRevert(token.connect(user).lockForSimulatedRedemption(redeemRef, UNIT));
    await token.connect(redeemer).burnPendingSimulatedPayout(redeemRef);
    await mustRevert(token.connect(reporter).recordSimulatedFiatSettlement(redeemRef, ethers.ZeroHash));
  });
});
