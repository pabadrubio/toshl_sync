# Pablo Abad 2017
#
# Toshl database program
from toshl.log import Log

class SyncApp:

    def __init__(self, token, decoder, database):
        self.token = token
        self.decoder = decoder
        self.database = database

    def run(self, transfers):
        for i in range(10):
            transfer = transfers[i]
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
        print '-----------------------------------------------'
        print 'A similar transfer was found:'
        transfer.prettyPrint()
        print '-----------------------------------------------'
        selection = raw_input("Overwrite? (Enter yes to overwrite)")
        return selection == "yes"