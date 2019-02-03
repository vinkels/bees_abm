from strategy.babee import babee_step
from strategy.rester import rester_step
from strategy.foraging import foraging_step
from strategy.scout import scout_step

BEE_STRATEGIES = {
    'babee': babee_step,
    'rester': rester_step,
    'foraging': foraging_step,
    'scout': scout_step
}