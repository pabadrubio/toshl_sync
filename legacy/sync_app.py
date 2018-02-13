# Pablo Abad 2017
#
# Toshl database program
from legacy.log import Log

class SyncApp:

    def __init__(self, token, decoder, database, doAskForOverwrite):
        self.token = token
        self.decoder = decoder
        self.database = database
        self.doAskForOverwrite = doAskForOverwrite

    def run(self, transfers):
        for transfer in transfers:
            self.handle_transfer(transfer)

    def handle_transfer(self, transfer):
        # Decode transfer
        decoded_transfer = self.decoder.try_to_decode(transfer)

        # Show transfer info
        if decoded_transfer is None:
            decoded_transfer = self.decoder.decode_with_feedback(transfer)

        Log.debug("Decoded transfer: " + str(decoded_transfer))

        # Check if the transfer is on the database (& send)
        if decoded_transfer is not None:
            similarTransfer = decoded_transfer.searchForSimilarTransferInToshl(self.token, self.database)
            if similarTransfer is not None and self.askForOverwrite(similarTransfer) == False:
                Log.debug("Skipping transfer because to a similar transfer was found.")
                return
            decoded_transfer.sendToToshl(self.token, self.database)
        else:
            Log.debug("Skipping transfer")

    def askForOverwrite(self, transfer):
        if self.doAskForOverwrite:
            print '-----------------------------------------------'
            print 'A similar transfer was found:'
            transfer.prettyPrint()
            print '-----------------------------------------------'
            selection = raw_input("Overwrite? (Enter yes to overwrite)")
            return selection == "yes"
        else:
            return False