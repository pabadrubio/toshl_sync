# Pablo Abad 2017
#
# Main program to update the tosh
import argparse
from toshl.ToshlApi import ToshlApi
from toshl.ApiToshlDatabase import ApiToshlDatabase
from toshl.ToshlSyncApp import ToshlSyncApp
from toshl.HintsFileClassifier import HintsFileClassifier
from toshl.SmartClassifer import SmartClassifier
from toshl.ComposedClassifier import ComposedClassifier
from toshl.INGTransfersLoader import INGTransfersLoader
from toshl.IOHandler import IOHandler
from toshl.FancyConsoleUI import FancyConsoleUI
from toshl.SimpleConsoleUI import SimpleConsoleUI

def read_token(token_file):
    with open(token_file, 'r') as f:
        token = f.read().strip()
    return token

def run(transfers_file, token_file, decoding_file, decoding_history, intellij_mode, account):
    token = read_token(token_file)
    if intellij_mode:
        io = IOHandler('utf-8', bufferGetChar=True)
    else:
        io = IOHandler('cp437')
    api = ToshlApi(token, io)
    database = ApiToshlDatabase(api)
    hintsClassifier = HintsFileClassifier(decoding_file)
    smartClassifier = SmartClassifier(decoding_history, True)
    classifier = ComposedClassifier([hintsClassifier, smartClassifier])
    transferLoader = INGTransfersLoader()
    transfers = transferLoader.loadTransfers(transfers_file)
    if intellij_mode:
        ui = SimpleConsoleUI(io, database)
    else:
        ui = FancyConsoleUI(io, database)
    app = ToshlSyncApp(database, classifier, ui, io, account, False)
    app.sync(transfers)

def main():
    parser = argparse.ArgumentParser(prog="toshl_sync", description='Synchronizes the Toshl account to a CSV transfers file')
    parser.add_argument('transfers_file')
    parser.add_argument('token_file')
    parser.add_argument('-df', '--decoding_file', default='data/DecodingHints.csv')
    parser.add_argument('-hcd', '--history_classifier_data', default='data/DecodingHistory.csv')
    parser.add_argument('-a', '--account', default='ING diba')
    parser.add_argument("--intellij", help="intellij console", action="store_true")
    args = parser.parse_args()
    run(args.transfers_file, args.token_file, args.decoding_file, args.history_classifier_data, args.intellij, args.account)

if __name__ == "__main__":
    main()
