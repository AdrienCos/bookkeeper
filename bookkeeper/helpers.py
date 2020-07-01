from typing import List, Tuple
from operator import itemgetter

from bookkeeper.sql import Session, Node, Sensor, Event, Attack, Measurement


def get_node_id(session: Session, name: str) -> int:
    """
    Returns the ID of the given node, or -1 if no node
    with this name is found.
    """
    node = session.query(Node.id).filter_by(name=name).all()
    if len(node) == 0:
        return -1
    node_id: int = node[0].id
    return node_id


def get_sensor_id(session: Session, name: str, node: str) -> int:
    """
    Returns the ID of the given sensor, or -1 if no sensor
    with this name is found.
    """
    node_id = get_node_id(session, node)
    sensor = session.query(Sensor.id).filter_by(
        name=name, node_id=node_id).all()
    if len(sensor) == 0:
        return -1
    return sensor[0].id


def get_all_nodes(session: Session) -> List[str]:
    """Returns the list of all nodes names stored in the database """
    nodes: list = session.query(Node.name).all()
    nodes_str: List[str] = [e.name for e in nodes]
    return nodes_str


def get_all_sensors(session: Session, node_name: str) -> List[str]:
    """Returns the list of all sensors for the given node in the database """
    node_id: int = get_node_id(session, node_name)
    if node_id == -1:
        return []
    sensors: list = session.query(Sensor.name).filter_by(node_id=node_id).all()
    sensors_str: List[str] = [e.name for e in sensors]
    return sensors_str


def get_sensor_unit(session: Session, node_name: str, sensor_name: str) -> str:
    """Returns the unit of the sensor"""
    sensor_id = get_sensor_id(session, sensor_name, node_name)
    if sensor_id == -1:
        return ""
    sensor = session.query(Sensor.unit).filter_by(id=sensor_id).all()
    return sensor[0].unit


def get_data_tuples_after_ts(session: Session, node_name: str, sensor_name: str, cutoff_ts: float) -> List[Tuple[float, float]]:
    """Returns the list of all data points for the given node/sensor after the given timestamp"""
    node_id: int = get_node_id(session, node_name)
    if node_id == -1:
        return []
    sensor_id: int = get_sensor_id(session, sensor_name, node_name)
    if sensor_id == -1:
        return []
    values: list = session.\
        query(Measurement.value, Measurement.timestamp).\
        filter_by(node_id=node_id, sensor_id=sensor_id).\
        filter(Measurement.timestamp >= cutoff_ts).\
        all()
    tuples: List[Tuple[float, float]] = [
        (e.timestamp, e.value) for e in values]
    tuples.sort(key=itemgetter(0))
    return tuples


def get_data_tuples_between_t1_t2(session: Session, node_name: str, sensor_name: str, t1: float, t2: float) -> List[Tuple[float, float]]:
    """Returns the list of all data points for the given node/sensor between the given timestamps"""
    node_id: int = get_node_id(session, node_name)
    if node_id == -1:
        return []
    sensor_id: int = get_sensor_id(session, sensor_name, node_name)
    if sensor_id == -1:
        return []
    values: list = session.\
        query(Measurement.value, Measurement.timestamp).\
        filter_by(node_id=node_id, sensor_id=sensor_id).\
        filter(Measurement.timestamp >= t1).\
        filter(Measurement.timestamp <= t2).\
        all()
    tuples: List[Tuple[float, float]] = [
        (e.timestamp, e.value) for e in values]
    tuples.sort(key=itemgetter(0))
    return tuples


def get_data_tuples(session: Session, node_name: str, sensor_name: str) -> List[Tuple[float, float]]:
    """Returns the list of all data points for the given node/sensor"""
    tuples: list = get_data_tuples_after_ts(session, node_name, sensor_name, 0)
    return tuples


def get_node_attacks_after_ts(session: Session, node_name: str, cutoff_ts: float) -> List[Tuple[float, int]]:
    """Returns a list of tuples of timestamp/attack_type of attacks after the given timestamp """
    node_id: int = get_node_id(session, node_name)
    if node_id == -1:
        return []
    attacks: List[Attack] = session.query(
        Attack.timestamp, Attack.attack_type).filter_by(node_id=node_id).all()
    attacks_all: List[Tuple[float, int]] = [
        (a.timestamp, a.attack_type) for a in attacks]
    attacks_cutoff: List[Tuple[float, int]] = [
        a for a in attacks_all if a[0] >= cutoff_ts]
    return attacks_cutoff


def get_node_attacks(session: Session, node_name: str) -> List[Tuple[float, int]]:
    """Returns a list of tuples of timestamp/attack_type"""
    attacks_list: list = get_node_attacks_after_ts(session, node_name, 0)
    return attacks_list


def get_node_events_after_ts(session: Session, node_name: str, cutoff_ts: float) -> List[Tuple[float, str]]:
    """Returns a list of tuples of timestamp/event_type of events after the given timestamp """
    node_id: int = get_node_id(session, node_name)
    if node_id == -1:
        return []
    events: List[Event] = session.query(
        Event.timestamp, Event.event_type).filter_by(node_id=node_id).all()
    events_all: List[Tuple[float, str]] = [
        (e.timestamp, e.event_type) for e in events
    ]
    events_cutoff: List[Tuple[float, str]] = [
        e for e in events_all if e[0] >= cutoff_ts
    ]
    return events_cutoff


def get_node_events(session: Session, node_name: str) -> List[Tuple[float, str]]:
    """Returns a list of tuples of timestamp/event_type of events """
    events: list = get_node_events_after_ts(session, node_name, 0)
    return events
