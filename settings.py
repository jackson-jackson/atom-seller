import poloniex
import private

POLO = poloniex.Poloniex(private.API_KEY,private.API_SECRET)

# Configuration
CURRENCY_PAIR = 'BTC_ATOM'
TARGET_VOLUME_DAY = 10 # Target amount of atoms that the script should sell per day
MIN_PRICE = 3 # Minimum atom price in USD that the script should sell at. Script will not sell below this
MIN_ORDER = .00015 #TODO make this based on min btc order size of .0001
OS = 'WINDOWS' # WINDOWS OR LINUX