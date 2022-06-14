from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, FundMe, exceptions
import pytest


def test_can_fund_and_withdrawl():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()

    transaction = fund_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    transaction2 = fund_me.withdrawl({"from": account})
    transaction2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdrawl():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")

    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    # fund_me.withdraw({"from": bad_actor})

    # If this execution reverts and raises an error thats good is what this is saying
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdrawl({"from": bad_actor})
