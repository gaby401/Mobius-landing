package net.corda.finance.contracts.asset

import net.corda.core.contracts.*
import net.corda.core.identity.AbstractParty
import net.corda.core.transactions.LedgerTransaction
import java.util.Currency

// $MOBI Token Contract
class MobiToken : Contract {
    companion object {
        const val ID = "net.corda.finance.contracts.asset.MobiToken"
        // Using USD as a placeholder because "MOBI" is not an ISO currency.
        val MOBI: Currency = Currency.getInstance("USD")
    }

    override fun verify(tx: LedgerTransaction) {
        // For MVP keep logic simple (no double spends beyond standard checks)
    }

    // Simple state for $MOBI balances
    data class State(
        val amount: Amount<Currency>,
        val owner: AbstractParty
    ) : ContractState {
        override val participants: List<AbstractParty> get() = listOf(owner)
    }
}
