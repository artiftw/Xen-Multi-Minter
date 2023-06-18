from web3 import Web3
from web3.middleware import geth_poa_middleware
from loguru import logger
from sys import stderr
from multiprocessing.dummy import Pool
#Import contract addresses
from common import XEN_MAIN,XEN_BSC,XEN_MATIC,XEN_AVAX,XEN_EVMOS,XEN_FTM,XEN_OKX
#Import RPC
from common import rpc_main,rpc_bsc,rpc_matic,rpc_avax,rpc_evmos,rpc_opt,rpc_ftm,rpc_okx
ABI = ''
c_addr = ''
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white>"
                          " | <level>{level: <8}</level>"
                          " | <cyan>{line}</cyan>"
                          " - <white>{message}</white>")


def send_tx(private_key: str):
    address = None

    try:
        address = Web3.toChecksumAddress(w3.eth.account.from_key(private_key).address)
        transaction = contract.functions.claimRank(lock_time) \
            .buildTransaction({
                'chainId': chain_id ,
                'from': address,
                'nonce': w3.eth.getTransactionCount(address)
            })

        signed_txn = w3.eth.account.signTransaction(transaction,
                                                    private_key=private_key)
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))

        logger.info(f'{address} | {tx_hash}')

    except Exception as error:
        logger.error(f'{address} | {error}')


if __name__ == '__main__':
    print('-' * 108)
    print((' '*46)+'XEN MULTI MINTER'+(' '*46))
    print('-' * 108)
    with open('accounts.txt', encoding='utf-8-sig') as file:
        private_keys = [row.strip() for row in file]

    with open('ABI.txt', 'r', encoding='utf-8-sig') as file:
        ABI = file.read().strip().replace('\n', '').replace(' ', '')
    print('Input chain:\n')
    print('1.Mainnet\n2.BSC Chain\n3.Polygon mainnet\n4.AVAX C-hain\n5.Evmos\n6.Fantom\n7.OKX\n')
    rpc_ch = int(input('Input Chain for mint XEN: '))
    if rpc_ch == 1:
        rpc = rpc_main
        c_addr = XEN_MAIN
    elif rpc_ch == 2:
        rpc = rpc_bsc
        c_addr = XEN_BSC
    elif rpc_ch == 3:
        rpc = rpc_matic
        c_addr = XEN_MATIC
    elif rpc_ch == 4:
        rpc= rpc_avax
        c_addr = XEN_AVAX
    elif rpc_ch == 5:
        rpc= rpc_evmos
        c_addr = XEN_EVMOS
    elif rpc_ch == 6:
        rpc= rpc_ftm
        c_addr = XEN_FTM
    elif rpc_ch == 7:
        rpc= rpc_okx
        c_addr = XEN_OKX

    w3 = Web3(Web3.HTTPProvider(rpc))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract = w3.eth.contract(address=Web3.toChecksumAddress(c_addr),
                               abi=ABI)
    chain_id = w3.eth.chain_id
    logger.info(f'Load {len(private_keys)} wallets')
    gwei = int(input('Input GWEI: '))
    lock_time = int(input('Input Unlock Period(DAYS): '))

    with Pool(processes=len(private_keys)) as executor:
        executor.map(send_tx, private_keys)

    input('Press Enter To Exit..')