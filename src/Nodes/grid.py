from abc import ABC
from dataclasses import dataclass
import numpy as np
from src.Nodes.consumer import Consumer
from src.Nodes.producer import Producer
from src.Nodes.node import Node, BalanceReturn, SettleReturn


@dataclass
class Protocol:
    node: Node
    transport_eff: float
    balance: float
    loss: float
    min_eff: float
    types_for_node: set


class Grid(Node):
    def clear_up(self, step: int):
        while self.protocols:
            (self.protocols.pop()).node.clear_up(step)

    def start(self, step) -> SettleReturn:
        balance_return = self.get_balance(step)
        result = self.start_settling(step, balance_return.balance)
        self.clear_up(step)
        return result

    # gives back (balance,loss)
    def get_balance(self, step: int) -> BalanceReturn:
        balance_returns: list[BalanceReturn] = [n.get_balance(step) for n in self.nodes]
        min_eff_consumer_producer = [1, 1]
        setTypes = {}
        for i in range(len(self.nodes)):
            types_for_node = balance_returns[i].types
            setTypes |= types_for_node

            ## calculating balance
            external_balance = balance_returns[i].balance
            transport_eff = self.transport_efficiencies[i]
            min_eff = transport_eff * balance_returns[i].min_eff

            if external_balance < 0:
                external_balance_after_transport = external_balance / transport_eff
                loss_on_link = -external_balance_after_transport + external_balance
                if min_eff < min_eff_consumer_producer[0]:
                    min_eff_consumer_producer[0] = min_eff
            else:
                external_balance_after_transport = external_balance * transport_eff
                loss_on_link = external_balance - external_balance_after_transport
                if min_eff < min_eff_consumer_producer[0]:
                    min_eff_consumer_producer[1] = min_eff

            self.local_balances[step] += external_balance_after_transport;
            external_loss_after_transport = loss_on_link + balance_returns[i].loss
            self.local_losses[step] += external_loss_after_transport
            protocol: Protocol = Protocol(self.nodes[i], transport_eff,
                                          external_balance_after_transport,
                                          external_loss_after_transport, min_eff,
                                          types_for_node)
            self.protocols.append(protocol)

        self.min_eff = min_eff_consumer_producer[self.local_balances[step] > 0]
        return BalanceReturn(self.local_balances[step], self.local_losses[step], self.min_eff, setTypes)

    def __init__(self, steps: int, nodes: list[Node], transport_efficiencies: list[float]):
        self.nodes = nodes
        self.transport_efficiencies = transport_efficiencies
        self.steps = steps
        self.local_balances = [0] * steps
        self.local_losses = [0] * steps
        self.min_eff = 1
        self.protocols: list[Protocol] = []

    # ToDo: Agam
    # import graph struckture from node x graph
    def import_graph_from_networkx(self, graph):
        pass

    # import graph from text json example in the wiki
    def import_graph_from_file(self, ):
        pass

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
        while updated_overflow != 0:
            result = self.settle(step, updated_overflow)
            updated_overflow = result.return_flow

        return result

    def settle(self, step, overflow) -> SettleReturn:
        overflow = overflow
        print(overflow)
        ##underproduction
        if overflow < 0:
            protocols_consumers = [p for p in
                                   self.protocols if
                                   p.balance < 0]
            protocols_consumers.sort(
                key=lambda x: x.balance)
            protocol = protocols_consumers.pop()
            self.protocols.remove(protocol)
            settle_return: SettleReturn = protocol.node.settle(
                step,
                overflow * protocol.transport_eff)

            updated_loss_on_transport = -settle_return.updated_external_balance * (1 / protocol.transport_eff - 1)
            # updating local values
            return_flow_after_transport = settle_return.return_flow / protocol.transport_eff
            self.local_balances[step] -= overflow - return_flow_after_transport
            self.local_losses[
                step] += -protocol.loss + settle_return.updated_external_loss + updated_loss_on_transport

            if not settle_return.settled:
                protocol.balance = settle_return.updated_external_balance / protocol.transport_eff
                protocol.loss = settle_return.updated_external_loss + updated_loss_on_transport
                protocol.min_eff = settle_return.updated_mineff * protocol.transport_eff
                self.protocols.append(protocol)
                protocols_consumers.append(protocol)

            if protocols_consumers:
                external_min_eff_after_transport = [p.min_eff for p in protocols_consumers]
                self.min_eff = min(external_min_eff_after_transport)
                return_settled = False
            else:
                self.min_eff = 1
                return_settled = True

            return SettleReturn(return_flow_after_transport, self.local_balances[step], self.local_losses[
                step], self.min_eff, return_settled)

        # overproduction
        # 1 Drop shit,
        # 2 load batterys
        # 3 decrease grean production

        else:
            # load batteries
            protocols_producer_batteries = [p for p in
                                            self.protocols if
                                            1 in p.types_for_node]

            if protocols_producer_batteries:
                # TODO batterie logic
                pass
            else:
                protocols_producers: Protocol = [p for p in self.protocols
                                                 if
                                                 p.balance > 0]
                protocols_producers.sort(
                    key=lambda p: p.min_eff)
                protocol = protocols_producers.pop()

                self.protocols.remove(protocol)
                settled_return: SettleReturn = protocol.node.settle(
                    step,
                    overflow / protocol.transport_eff)

                update_loss_on_transport = (1 - protocol.transport_eff) * settled_return.updated_external_balance
                return_flow_after_transport = settled_return.return_flow * protocol.transport_eff
                self.local_balances[step] -= overflow - return_flow_after_transport
                self.local_losses[
                    step] += - protocol.loss + settled_return.updated_external_loss + update_loss_on_transport

                if not settled_return.settled:
                    protocol.balance = settled_return.updated_external_balance * protocol.transport_eff
                    protocol.min_eff = settled_return.updated_mineff * protocol.transport_eff
                    protocol.loss = settled_return.updated_external_loss + update_loss_on_transport,
                    self.protocols.append(protocol)
                    protocols_producers.append(protocol)

                if protocols_producers:
                    external_min_eff_after_transport = [p.min_eff for p in protocols_producers]
                    self.min_eff = min(external_min_eff_after_transport)
                    return_settled = False
                else:
                    self.min_eff = 1
                    return_settled = True

                return SettleReturn(return_flow_after_transport, self.local_balances[step], self.local_losses[
                    step], self.min_eff, return_settled)
