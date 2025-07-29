package net.corda.finance.flows

import co.paralleluniverse.fibers.Suspendable
import net.corda.core.contracts.Amount
import net.corda.core.contracts.Command
import net.corda.core.flows.*
import net.corda.core.identity.Party
import net.corda.core.transactions.SignedTransaction
import net.corda.core.transactions.TransactionBuilder
import net.corda.finance.contracts.asset.MobiToken
import java.util.Currency

// Flow to issue $MOBI tokens
@InitiatingFlow
@StartableByRPC
class MobiIssueFlow(
    private val amount: Amount<Currency>,
    private val recipient: Party
) : FlowLogic<SignedTransaction>() {

    @Suspendable
    override fun call(): SignedTransaction {
        // Choose notary
        val notary = serviceHub.networkMapCache.notaryIdentities.first()

        // Build the output state
        val outputState = MobiToken.State(amount, recipient)

        // Command to issue MOBI
        val issueCommand = Command(MobiToken::class.java, ourIdentity.owningKey)

        // Build transaction
        val txBuilder = TransactionBuilder(notary)
            .addOutputState(outputState, MobiToken.ID)
            .addCommand(issueCommand)

        // Verify and sign
        txBuilder.verify(serviceHub)
        val signedTx = serviceHub.signInitialTransaction(txBuilder)

        // Finalise and distribute
        return subFlow(FinalityFlow(signedTx, emptyList()))
    }
}
