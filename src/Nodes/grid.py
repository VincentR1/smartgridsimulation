from collections import Counter
from dataclasses import dataclass
from src.Nodes.node import Node, BalanceReturn, SettleReturn, StorageInfo
from src.Nodes.types import NodeTypes


@dataclass
class Protocol:
    node: Node
    transport_eff: float
    balance: float
    loss: float
    min_eff: float
    types: Counter
    storage: StorageInfo


class Grid(Node):
    def clear_up(self, step: int):
        self.balance_calculated.pop()
        while self.protocols:
            (self.protocols.pop()).node.clear_up(step)

    def start(self, step) -> SettleReturn:
        balance_return = self.get_balance(step)
        result = self.start_settling(step, balance_return.balance)
        self.clear_up(step)
        return result

    def run_simulation(self):
        for i in range(len(self.local_balances)):
            self.start(i)

    # gives back (balance,loss)
    def get_balance(self, step: int) -> BalanceReturn:
        if self.balance_calculated:
            return self.balance_calculated[0]
        else:
            self.local_balances[step] = 0
            self.local_losses[step] = 0
            self.protocols = []
            balance_returns = [n.get_balance(step) for n in self.nodes]
            min_eff_consumer = 1
            min_eff_producer = 1
            setTypes = Counter()
            storage = StorageInfo(load=0, capacity=0, min_dist_consumer=0, min_dist_producer=0)
            min_dist_storage_consumer_fixed = 0
            min_dist_storage_consumer_opt = 0
            min_dist_storage_producer_fixed = 0
            min_dist_storage_producer_opt = 0
            for i in range(len(self.nodes)):
                balance_returns_for_node = balance_returns[i]
                types_for_node = balance_returns_for_node.types
                setTypes.update(types_for_node)
                ## calculating balance
                external_balance = balance_returns[i].balance
                transport_eff = self.transport_efficiencies[i]
                min_eff = transport_eff * balance_returns[i].min_eff

                if external_balance < 0:
                    external_balance_after_transport = external_balance / transport_eff
                    loss_on_link = -external_balance_after_transport + external_balance
                    if min_eff < min_eff_consumer:
                        min_eff_consumer = min_eff
                else:
                    external_balance_after_transport = external_balance * transport_eff
                    loss_on_link = external_balance - external_balance_after_transport
                    if min_eff < min_eff_producer:
                        min_eff_producer = min_eff

                self.local_balances[step] += external_balance_after_transport
                external_loss_after_transport = loss_on_link + balance_returns[i].loss
                self.local_losses[step] += external_loss_after_transport
                storage_for_node = balance_returns[i].storage

                if storage_for_node.min_dist_producer > 0:
                    min_dist_storage_producer_for_node = storage_for_node.min_dist_producer
                    if min_dist_storage_producer_for_node > min_dist_storage_producer_fixed:
                        min_dist_storage_producer_fixed = min_dist_storage_producer_for_node
                else:
                    min_dist_storage_producer_for_node = storage_for_node.min_dist_producer * transport_eff
                    if min_dist_storage_producer_for_node < min_dist_storage_producer_opt:
                        min_dist_storage_producer_opt = min_dist_storage_producer_for_node

                if storage_for_node.min_dist_consumer > 0:
                    min_dist_storage_consumer_for_node = storage_for_node.min_dist_producer
                    if min_dist_storage_consumer_for_node > min_dist_storage_consumer_fixed:
                        min_dist_storage_consumer_fixed = min_dist_storage_consumer_for_node
                else:
                    min_dist_storage_consumer_for_node = storage_for_node.min_dist_producer * transport_eff
                    if min_dist_storage_consumer_for_node < min_dist_storage_consumer_opt:
                        min_dist_storage_consumer_opt = min_dist_storage_consumer_for_node

                node_capacity_after_transport = storage_for_node.capacity / transport_eff
                storage.capacity += node_capacity_after_transport

                node_load_after_transport = storage_for_node.load * transport_eff
                storage.load += node_load_after_transport
                storage_after_transport = StorageInfo(load=node_load_after_transport,
                                                      capacity=node_capacity_after_transport,
                                                      min_dist_consumer=min_dist_storage_consumer_for_node,
                                                      min_dist_producer=min_dist_storage_producer_for_node)

                protocol: Protocol = Protocol(node=self.nodes[i],
                                              transport_eff=transport_eff,
                                              balance=external_balance_after_transport,
                                              loss=external_loss_after_transport,
                                              min_eff=min_eff,
                                              types=types_for_node,
                                              storage=storage_after_transport)

                self.protocols.append(protocol)

            if self.local_balances[step] > 0:
                self.min_eff = min_eff_producer
                min_dist_storage_producer_opt *= -1
                storage.min_dist_producer = min_dist_storage_producer_opt \
                    if min_dist_storage_producer_opt > min_dist_storage_producer_fixed \
                    else min_dist_storage_producer_fixed
                storage.min_dist_consumer = min_dist_storage_consumer_fixed \
                    if min_dist_storage_consumer_fixed > 0 else min_dist_storage_consumer_opt

            elif self.local_balances[step] < 0:
                self.min_eff = min_eff_consumer
                min_dist_storage_consumer_opt *= -1
                storage.min_dist_consumer = min_dist_storage_consumer_opt \
                    if min_dist_storage_consumer_opt > min_dist_storage_consumer_fixed \
                    else min_dist_storage_consumer_fixed
                storage.min_dist_producer = min_dist_storage_producer_fixed \
                    if min_dist_storage_producer_fixed > 0 else min_dist_storage_producer_opt
            else:
                self.min_eff = min_eff_consumer
                storage.min_dist_consumer = min_dist_storage_consumer_fixed \
                    if min_dist_storage_consumer_fixed > 0 else min_dist_storage_consumer_opt
                storage.min_dist_producer = min_dist_storage_producer_fixed \
                    if min_dist_storage_producer_fixed > 0 else min_dist_storage_producer_opt
            self.balance_calculated.append(
                BalanceReturn(balance=self.local_balances[step], loss=self.local_losses[step], min_eff=self.min_eff,
                              storage=storage, types=setTypes))

            return self.balance_calculated[0]

    def __init__(self, steps: int, nodes: list[Node], transport_efficiencies: list[float]):
        self.nodes = nodes
        self.transport_efficiencies = transport_efficiencies
        self.steps = steps
        self.local_balances = [0] * steps
        self.local_losses = [0] * steps
        self.min_eff = 1
        self.protocols: list[Protocol] = []
        self.balance_calculated: list[BalanceReturn] = []

    # Adding one node to a Grid
    def adding_node(self, node: Node, transport_eff: float):
        self.nodes.append(node)
        self.transport_efficiencies.append(transport_eff)

    def adding_nodes(self, nodes: list[Node], trasport_effs: list[float]):
        if len(nodes) != len(trasport_effs):
            raise Exception("Arrays length are not matching")
        self.nodes += nodes
        self.transport_efficiencies += trasport_effs

    def start_settling(self, step, overflow):
        updated_overflow = overflow
        while updated_overflow < - 0.05 or updated_overflow > 0.05:
            self.settle(step, updated_overflow),
            balance_return = self.get_balance(step)
            updated_overflow = balance_return.balance

    def settle(self, step, overflow):
        overflow = overflow
        overflow_after_transport: float
        protocol: Protocol
        local_balance_return = self.balance_calculated.pop()
        if overflow < 0:
            # discharge batteries
            protocol_with_load = [p for p in self.protocols if p.storage.load > 0]
            # chose the one closest to counsumer
            if protocol_with_load:
                protocol_with_load.sort(key=lambda x: x.storage.min_dist_consumer)
                protocol = protocol_with_load[-1]
                if protocol.storage.min_dist_consumer < 0:
                    protocol = protocol_with_load[0]
                max_overflow = local_balance_return.balance if local_balance_return.balance < 0 else overflow

                if protocol.balance < 0:
                    overflow_after_transport = max_overflow * protocol.transport_eff
                else:
                    overflow_after_transport = max_overflow / protocol.transport_eff
            else:

                protocol_with_extern = [p for p in self.protocols if NodeTypes.EXTERN in p.types]
                if protocol_with_extern:
                    protocol = protocol_with_extern.pop()
                    if protocol.balance < 0:
                        overflow_after_transport = overflow * protocol.transport_eff
                    else:
                        overflow_after_transport = overflow / protocol.transport_eff

                # chose consumer
                else:
                    protocol_consumers = [p for p in self.protocols if p.balance < 0]
                    protocol_consumers.sort(key=lambda x: x.min_eff)
                    protocol = protocol_consumers[0]
                    overflow_after_transport = overflow * protocol.transport_eff

        else:
            # coal
            protocol_with_coal = [p for p in self.protocols if NodeTypes.COAL in p.types]
            if protocol_with_coal:
                protocol_with_coal.sort(key=lambda x: x.min_eff)
                protocol = protocol_with_coal[0]
                max_overflow = overflow

            # load batteries
            else:
                protocol_with_capacity = [p for p in self.protocols if p.storage.capacity > 0]
                if protocol_with_capacity:
                    protocol_with_capacity.sort(key=lambda x: x.storage.min_dist_producer)
                    protocol = protocol_with_capacity[-1]
                    if protocol.storage.min_dist_producer < 0:
                        protocol = protocol_with_capacity[0]
                    max_overflow = local_balance_return.balance if local_balance_return.balance > 0 else overflow

                else:
                    protocol_extern = [p for p in self.protocols if NodeTypes.EXTERN in p.types]
                    if protocol_extern:
                        protocol = protocol_extern.pop()
                        max_overflow = overflow
                    else:
                        protocol_producers = [p for p in self.protocols if p.balance > 0]
                        protocol_producers.sort(key=lambda x: x.min_eff)
                        protocol = protocol_producers[0]
                        max_overflow = overflow

            if protocol.balance > 0:
                overflow_after_transport = max_overflow / protocol.transport_eff
            else:
                overflow_after_transport = max_overflow * protocol.transport_eff

        protocol.node.settle(step, overflow_after_transport)
