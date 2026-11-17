"""Spike related utils classes"""
from texttable import Texttable

class SpikeEvent:
    """contains originator neuron, charge and target neurons"""
    def __init__(self, nid, charge, targets):
        self.nid = nid
        self.charge = charge
        self.targets = targets

class TransformationRule:
    """
    # regex are in the form: a^mod (a^div)^*
    """
    def __init__(self, div, mod, source, target, delay):
        # Layer-1, layer-2, layer-3 rules' syntax: 
        # div, mod, minimum_charge_value, emitted_spikes, delay

        # div    <--> div
        self.div = div # looped "a" in the regex
        # mod    <--> mod
        self.mod = mod # basic "a" in the regex
        # source <--> minimum_charge_value
        self.source = source # spike consumed when the rule applies
        # target <--> emitted_spikes
        self.target = target # spike fired when the rule applies
        # delay  <--> delay
        self.delay = delay # refractory period of the rules

    def check(self, charge):
        """Returns true if the tranformation rule can be activated considering 
        given neuron's charge. Returns false otherwise."""

        #with div and mod is possible to manage all value condition for charge
        # (1) Managing negative rules (with negative charge): charge < 0
        # (2) & (3) Checking if regex admits negative numbers: self.div < 0 or self.mod < 0
        if charge < 0 and (self.div < 0 or self.mod < 0): #neuron contains anti-spikes
            if self.div == 0:
                # (1) div * k + mod = charge --> mod = charge
                return charge == self.mod
            else:
                # (1) div * k + mod = charge
                return (self.mod - charge) % -self.div == 0

        # (1) Managing positive rules (with positive charge): charge > 0
        # (2) Checking if charge is >= than the minimum value defined by the regex: charge >= self.mod
        # (3) Checking if neuron can emit at least the required amount of energy: charge >= self.target
        # Neurons should emit only as much energy as they have (membrane potential)
        if charge > 0 and charge >= self.mod and charge >= self.target: #for avoid negative values
            if self.div > 0:
                # (1) Checking minimum charge value to trigger the rule: charge >= self.source
                # (2) div * k + mod = charge
                return charge >= self.source and (charge - self.mod) % self.div == 0
            if self.div == 0:
                # (1) Checking minimum charge value to trigger the rule: charge >= self.source
                # (2) div * k + mod = charge --> mod = charge
                return charge >= self.source and charge == self.mod
            
        return False

    # exec() not used in the project
    def exec(self, charge):
        return charge - self.source

    def __str__(self):
        # Build the condition part of the rule, e.g., "2a+1" if div=2 and mod=1
        rulecond = "{0}a{1}".format(self.div, "+{0}".format(self.mod) if self.mod > 0 else "")

        # Build the transformation part: "source->target"
        # If target > 0, append "!" to indicate a firing rule (sends spike)
        # If target == 0, it's a forgetting rule (consumes charge only)
        ruletransf = "{0}->{1}{2}".format(self.source, self.target, "!" if self.target > 0 else "")

        # Final string format: condition;transformation;delay
        return "{0};{1};{2}".format(rulecond, ruletransf, self.delay)

class History:
    """
    responsible for recording each neuron status at each step
    takes of advantage of neuron ids starting from 0
    """
    def __init__(self, neurons):
        """Initializing a History instance as a 2-d array, with rows as the state 
        of the entire system during each tick and columns as the evolving state of the
        singular neuron, including activated rules, current charge and external 
        related activities."""
    
        self.ticks = [] # every element is the state of a neuron
        self.n_len = len(neurons)

        self.add_new_tick() # add initial charge
        for neuron in neurons:
            self.ticks[-1][neuron.nid] = neuron.charge

    def add_new_tick(self):
        self.ticks.append([""] * self.n_len)

    def record_rule(self, neuron, used_rule):
        """Recording the current internal state of the neuron."""
        self.ticks[-1][neuron.nid] = "r:{0}\nc:{1}".format(str(used_rule) if used_rule else "-", neuron.charge)

    def record_incoming(self, neuron, charge, source_nid):
        """Recording an external activity related to the neuron."""
        self.ticks[-1][neuron.nid] += "\ni:{0}({2})\nc:{1}".format(charge, neuron.charge, source_nid)

    # Create and populate output table
    def __str__(self):
        ticks_wrapper = []
        for idx, tick in enumerate(self.ticks):
            # Managing initial prefix
            pref = idx - 1 if idx > 0 else "initial\ncharge"
            ticks_wrapper.append([pref] + tick)

        table = Texttable()
        table.set_cols_width([7] + [20] * len(self.ticks[0]))
        table.header(["Step"] + ["Neuron " + str(nid) for nid in range(len(self.ticks[0]))])
        table.add_rows(ticks_wrapper[:], header=False)

        return str(table.draw())
        