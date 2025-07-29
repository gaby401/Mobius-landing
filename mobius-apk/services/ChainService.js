import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('mobius.db');

const ChainService = {
  init: () =>
    new Promise((resolve) => {
      db.transaction(tx => {
        tx.executeSql(
          'CREATE TABLE IF NOT EXISTS blocks (id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, timestamp TEXT);'
        );
        tx.executeSql(
          'CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, block_id INTEGER, from_addr TEXT, to_addr TEXT, amount REAL);'
        );
      }, null, resolve);
    }),

  addTransaction: (tx) =>
    new Promise((resolve) => {
      db.transaction(txn => {
        txn.executeSql(
          'INSERT INTO transactions (block_id, from_addr, to_addr, amount) VALUES (?, ?, ?, ?);',
          [0, tx.from, tx.to, tx.amount],
          () => resolve()
        );
      });
    }),

  mineBlock: (miner) =>
    new Promise((resolve) => {
      const timestamp = new Date().toISOString();
      const hash = `hash_${Date.now()}`;
      db.transaction(txn => {
        txn.executeSql(
          'INSERT INTO blocks (hash, timestamp) VALUES (?, ?);',
          [hash, timestamp],
          (_, result) => {
            const blockId = result.insertId;
            txn.executeSql(
              'UPDATE transactions SET block_id = ? WHERE block_id = 0;',
              [blockId],
              () => resolve()
            );
          }
        );
      });
    }),

  getBalanceOfAddress: (address) =>
    new Promise((resolve) => {
      db.transaction(tx => {
        tx.executeSql(
          'SELECT SUM(CASE WHEN to_addr = ? THEN amount ELSE 0 END) - SUM(CASE WHEN from_addr = ? THEN amount ELSE 0 END) as balance FROM transactions;',
          [address, address],
          (_, { rows }) => resolve(rows.item(0).balance || 0)
        );
      });
    }),

  getBlocksWithTransactions: () =>
    new Promise((resolve) => {
      db.transaction(tx => {
        tx.executeSql('SELECT * FROM blocks ORDER BY id DESC;', [], (_, { rows }) => {
          const blocks = rows._array;
          const promises = blocks.map(block =>
            new Promise((res) => {
              tx.executeSql(
                'SELECT * FROM transactions WHERE block_id = ?;',
                [block.id],
                (_, { rows }) => {
                  block.transactions = rows._array;
                  res();
                }
              );
            })
          );
          Promise.all(promises).then(() => resolve(blocks));
        });
      });
    }),
};

export default ChainService;
