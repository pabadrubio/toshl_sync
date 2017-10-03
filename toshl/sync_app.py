# Pablo Abad 2017
#
# Toshl database program
from toshl.log import Log

class SyncApp:

    def __init__(self, token, decoder):
        self.token = token
        self.decoder = decoder

    def run(self, transfers):
        for i in range(10):
            transfer = transfers[i]
            self.handle_transfer(transfer)

    def handle_transfer(self, transfer):
        # Decode transfer
        decoded_transfer = self.decoder.try_to_decode(transfer)
        Log.debug("Decoded transfer: " + str(decoded_transfer))

        # Show transfer info
        if decoded_transfer is None:
            decoded_transfer = self.decoder.decode_with_feedback(transfer)

        # Check if the transfer is on the database (& send)
        if decoded_transfer is not None:
            similarTransfer = decoded_transfer.searchForSimilarTransferInToshl()
            if similarTransfer is not None and self.askForOverwrite(similarTransfer) == False:
                return
            decoded_transfer.sendToToshl(self.token)

    def askForOverwrite(self):
        return False