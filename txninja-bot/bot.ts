// @ts-nocheck
import TelegramBot from 'node-telegram-bot-api'
import { TransactionFactory } from './tx-builder/transactionFactory'
import { Common } from '@ethereumjs/common'
import { Chain, Hardfork } from '@ethereumjs/common/dist/chains'
import { hexlify, arrayify } from 'ethereum-cryptography/utils'

// === CONFIG ===
const bot = new TelegramBot('8287665307:AAHasM3sFw9ix7T1OcTIta6eYRlkjLUDkOg', { polling: true })
const common = new Common({ chain: Chain.Mainnet, hardfork: Hardfork.London })

bot.onText(/\/tx (.+)/, async (msg, match) => {
  const chatId = msg.chat.id
  const args = match?.[1]?.split(' ').reduce((acc, cur) => {
    const [k, v] = cur.split('=')
    acc[k] = v
    return acc
  }, {} as Record<string, string>)

  if (!args?.to || !args?.value) {
    return bot.sendMessage(chatId, `❌ Usage: /tx to=<address> value=<amount> [type=0|1|2|3]`)
  }

  try {
    const txData = {
      to: arrayify(args.to),
      value: BigInt(parseFloat(args.value) * 1e18),
      gasLimit: BigInt(21000),
      maxFeePerGas: BigInt(2000000000),
      maxPriorityFeePerGas: BigInt(1000000000),
      nonce: BigInt(0),
    }

    const type = parseInt(args?.type || '2')
    const tx = TransactionFactory.fromTxData(txData, { common, freeze: false, type })

    bot.sendMessage(chatId, `✅ TX built!\n\nHex: ${hexlify(tx.serialize())}`)
  } catch (err) {
    bot.sendMessage(chatId, `❌ TX error: ${err.message}`)
  }
})
