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

// Flow to transfer $MOBI tokens between two parties
@InitiatingFlow
@StartableByRPC
class MobiTransferFlow(
    private val amount: Amount<Currency>,
    private val newOwner: Party
) : FlowLogic<SignedTransaction>() {

    @Suspendable
    override fun call(): SignedTransaction {
        // Choose a notary
        val notary = serviceHub.networkMapCache.notaryIdentities.first()

        // Build output state
        val outputState = MobiToken.State(amount, newOwner)

        // Create command for MOBI transfer
        val transferCommand = Command(MobiToken::class.java, ourIdentity.owningKey)

        // Build transaction
        val txBuilder = TransactionBuilder(notary)
            .addOutputState(outputState, MobiToken.ID)
            .addCommand(transferCommand)

        // Verify and sign
        txBuilder.verify(serviceHub)
        val signedTx = serviceHub.signInitialTransaction(txBuilder)

        // Collect counterparty signature (if needed)
        val sessions = listOf(initiateFlow(newOwner))

        // Finalise and distribute
        return subFlow(FinalityFlow(signedTx, sessions))
    }
}

@InitiatedBy(MobiTransferFlow::class)
class MobiTransferFlowResponder(private val counterpartySession: FlowSession) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {
        return subFlow(ReceiveFinalityFlow(counterpartySession))
    }
}
