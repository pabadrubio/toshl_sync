# Pablo Abad 2017
#
# Main program to update the tosh
import argparse, requests
from toshl.database import ToshlDatabase
from toshl.csvfile import loadCSVTransfersFile
from toshl.decoding import Decoder
from toshl.sync_app import SyncApp


def read_token(token_file):
    with open(token_file, 'r') as f:
        token = f.read().strip()
    return token


def run(transfers_file, token_file, decoding_file, decoding_history, account):
    token = read_token(token_file)
    database = ToshlDatabase(token)
    decoder = Decoder(database, decoding_file, decoding_history, account)
    transfers = loadCSVTransfersFile(transfers_file)
    app = SyncApp(token, decoder, database)
    app.run(transfers)
    #database.listTransfers(token)

def main():
    parser = argparse.ArgumentParser(prog="toshl_sync", description='Synchronizes the Toshl account to a CSV transfers file')
    parser.add_argument('transfers_file')
    parser.add_argument('token_file')
    parser.add_argument('--decoding_file', default='data/DecodingHints.csv')
    parser.add_argument('--decoding_history', default='data/DecodingHistory.csv')
    parser.add_argument('--account', default='ING diba')
    args = parser.parse_args()
    run(args.transfers_file, args.token_file, args.decoding_file, args.decoding_history, args.account)

if __name__ == "__main__":
    main()
