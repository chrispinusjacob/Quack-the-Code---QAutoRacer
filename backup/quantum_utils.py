import numpy as np
import random
import math
from collections import deque

class QuantumSimulator:
    """
    A class that simulates quantum computing behavior for game mechanics
    without requiring actual quantum hardware.
    """
    
    def __init__(self, num_qubits=3):
        """Initialize the quantum simulator with a specified number of qubits"""
        self.num_qubits = num_qubits
        self.state_history = deque(maxlen=100)  # Store recent states for patterns
        self.entanglement_matrix = np.random.random((num_qubits, num_qubits))
        self.phase_shifts = np.zeros(num_qubits)
        
        # Initialize with a random quantum state
        self.reset_state()
    
    def reset_state(self):
        """Reset to a new random quantum state"""
        # Create a random state vector
        self.state = np.random.random(2**self.num_qubits) + 1j * np.random.random(2**self.num_qubits)
        # Normalize the state vector
        self.state = self.state / np.sqrt(np.sum(np.abs(self.state)**2))
        self.state_history.append(np.copy(self.state))
    
    def apply_hadamard(self, qubit_index):
        """Apply a Hadamard gate to put a qubit in superposition"""
        # Simplified Hadamard implementation for simulation
        dim = 2**self.num_qubits
        new_state = np.zeros(dim, dtype=complex)
        
        for i in range(dim):
            # Check if the qubit_index bit is 0 or 1
            if (i >> qubit_index) & 1:
                # If 1, add and subtract
                new_state[i] += self.state[i] / np.sqrt(2)
                new_state[i ^ (1 << qubit_index)] -= self.state[i] / np.sqrt(2)
            else:
                # If 0, add and add
                new_state[i] += self.state[i] / np.sqrt(2)
                new_state[i ^ (1 << qubit_index)] += self.state[i] / np.sqrt(2)
        
        self.state = new_state
        self.state_history.append(np.copy(self.state))
    
    def apply_phase_shift(self, qubit_index, theta):
        """Apply a phase shift to a qubit"""
        dim = 2**self.num_qubits
        for i in range(dim):
            if (i >> qubit_index) & 1:
                self.state[i] *= np.exp(1j * theta)
        
        self.phase_shifts[qubit_index] = theta
        self.state_history.append(np.copy(self.state))
    
    def entangle_qubits(self, qubit1, qubit2):
        """Entangle two qubits (simplified simulation)"""
        if qubit1 == qubit2:
            return
            
        # Update entanglement matrix
        self.entanglement_matrix[qubit1, qubit2] = random.random()
        self.entanglement_matrix[qubit2, qubit1] = self.entanglement_matrix[qubit1, qubit2]
        
        # Apply a simplified CNOT-like operation
        dim = 2**self.num_qubits
        new_state = np.copy(self.state)
        
        for i in range(dim):
            if (i >> qubit1) & 1:
                # Flip qubit2 if qubit1 is 1
                new_state[i], new_state[i ^ (1 << qubit2)] = new_state[i ^ (1 << qubit2)], new_state[i]
        
        self.state = new_state
        self.state_history.append(np.copy(self.state))
    
    def measure(self, qubit_index=None):
        """
        Measure a specific qubit or the entire system
        Returns 0 or 1 for a specific qubit, or the collapsed state index
        """
        if qubit_index is not None:
            # Measure specific qubit
            prob_one = 0
            dim = 2**self.num_qubits
            
            for i in range(dim):
                if (i >> qubit_index) & 1:
                    prob_one += np.abs(self.state[i])**2
            
            # Collapse the state based on measurement
            result = 1 if random.random() < prob_one else 0
            
            # Update state vector to reflect measurement
            new_state = np.zeros(dim, dtype=complex)
            norm = 0
            
            for i in range(dim):
                bit_val = (i >> qubit_index) & 1
                if bit_val == result:
                    new_state[i] = self.state[i]
                    norm += np.abs(self.state[i])**2
            
            if norm > 0:
                self.state = new_state / np.sqrt(norm)
            
            self.state_history.append(np.copy(self.state))
            return result
        else:
            # Measure entire system
            probabilities = np.abs(self.state)**2
            result = np.random.choice(len(probabilities), p=probabilities)
            
            # Collapse state to the measured state
            new_state = np.zeros_like(self.state)
            new_state[result] = 1.0
            self.state = new_state
            
            self.state_history.append(np.copy(self.state))
            return result
    
    def get_quantum_random(self, min_val=0, max_val=1):
        """Generate a quantum random number between min_val and max_val"""
        # Apply some quantum operations to mix things up
        qubit = random.randint(0, self.num_qubits - 1)
        self.apply_hadamard(qubit)
        
        # Measure a random qubit
        measurement = self.measure(random.randint(0, self.num_qubits - 1))
        
        # Use the phase information to get more randomness
        phase_factor = np.sum(np.abs(self.phase_shifts)) / (2 * np.pi)
        
        # Combine measurement with phase information
        random_val = (measurement + phase_factor) % 1.0
        
        # Scale to desired range
        return min_val + random_val * (max_val - min_val)
    
    def get_quantum_decision(self, options, weights=None):
        """
        Make a quantum decision among multiple options
        options: list of possible choices
        weights: optional probability weights
        """
        if weights is None:
            # Equal probability for all options
            weights = [1.0 / len(options)] * len(options)
        
        # Normalize weights
        total = sum(weights)
        weights = [w / total for w in weights]
        
        # Apply quantum operations to introduce quantum randomness
        for i in range(min(self.num_qubits, len(options))):
            self.apply_hadamard(i)
            self.apply_phase_shift(i, random.random() * 2 * np.pi)
        
        # Entangle some qubits for more quantum effects
        if self.num_qubits >= 2:
            self.entangle_qubits(0, 1)
        
        # Measure the system
        result = self.measure()
        
        # Map the measurement result to an option index using the weights
        cumulative_weights = [sum(weights[:i+1]) for i in range(len(weights))]
        random_val = (result / (2**self.num_qubits - 1))
        
        for i, threshold in enumerate(cumulative_weights):
            if random_val <= threshold:
                return options[i]
        
        # Fallback
        return random.choice(options)
    
    def get_quantum_difficulty(self, base_difficulty, variance=0.3):
        """
        Generate a difficulty level based on quantum superposition
        base_difficulty: the center point of difficulty (0.0 to 1.0)
        variance: how much the difficulty can vary (0.0 to 1.0)
        """
        # Apply Hadamard gates to create superposition
        for i in range(self.num_qubits):
            self.apply_hadamard(i)
        
        # Apply phase shifts based on current game state
        for i in range(self.num_qubits):
            self.apply_phase_shift(i, random.random() * 2 * np.pi)
        
        # Entangle qubits to create complex quantum states
        if self.num_qubits >= 2:
            for i in range(self.num_qubits - 1):
                self.entangle_qubits(i, i + 1)
        
        # Measure to collapse the superposition
        measurements = [self.measure(i) for i in range(self.num_qubits)]
        
        # Convert binary measurements to a value between -variance and +variance
        binary_val = sum(m * (2**i) for i, m in enumerate(measurements))
        max_val = 2**self.num_qubits - 1
        offset = (binary_val / max_val) * 2 * variance - variance
        
        # Apply the offset to the base difficulty
        difficulty = base_difficulty + offset
        
        # Clamp to valid range
        return max(0.0, min(1.0, difficulty))
    
    def quantum_teleport(self, current_pos, possible_positions, max_distance):
        """
        Simulate quantum teleportation for game mechanics
        current_pos: current position (x, y)
        possible_positions: list of possible positions to teleport to
        max_distance: maximum teleportation distance
        
        Returns: new position after teleportation
        """
        # Filter positions by maximum distance
        valid_positions = []
        for pos in possible_positions:
            distance = math.sqrt((pos[0] - current_pos[0])**2 + (pos[1] - current_pos[1])**2)
            if distance <= max_distance:
                valid_positions.append(pos)
        
        if not valid_positions:
            return current_pos  # No valid teleportation targets
        
        # Apply quantum operations
        for i in range(self.num_qubits):
            self.apply_hadamard(i)
        
        # Entangle qubits
        if self.num_qubits >= 2:
            self.entangle_qubits(0, self.num_qubits - 1)
        
        # The measurement collapses the superposition to select a position
        index = self.measure() % len(valid_positions)
        return valid_positions[index]
    
    def get_quantum_achievement_score(self, base_score, performance_metrics):
        """
        Calculate an achievement score using quantum algorithms
        base_score: the starting score
        performance_metrics: dict of player performance metrics
        
        Returns: quantum-enhanced score
        """
        # Apply quantum operations based on performance metrics
        for i, (metric, value) in enumerate(performance_metrics.items()):
            qubit_idx = i % self.num_qubits
            # Apply operations based on the metric value
            if value > 0.5:  # Good performance
                self.apply_hadamard(qubit_idx)
                self.apply_phase_shift(qubit_idx, value * np.pi)
            else:  # Poor performance
                self.apply_phase_shift(qubit_idx, value * np.pi / 2)
        
        # Entangle qubits to create complex quantum states
        if self.num_qubits >= 2:
            for i in range(self.num_qubits - 1):
                self.entangle_qubits(i, (i + 1) % self.num_qubits)
        
        # Measure the quantum state
        measurements = [self.measure(i) for i in range(self.num_qubits)]
        
        # Calculate quantum bonus based on measurements
        quantum_factor = sum(m * (2**i) for i, m in enumerate(measurements)) / (2**self.num_qubits - 1)
        quantum_bonus = quantum_factor * 0.5  # Up to 50% bonus
        
        # Apply quantum bonus to base score
        return int(base_score * (1 + quantum_bonus))

# Quantum event system for game events
class QuantumEventSystem:
    def __init__(self, num_qubits=3):
        self.quantum_sim = QuantumSimulator(num_qubits)
        self.event_cooldowns = {}
        self.event_history = []
    
    def register_event(self, event_name, min_cooldown=0, max_cooldown=0):
        """Register a new event type with cooldown range"""
        self.event_cooldowns[event_name] = {
            'min': min_cooldown,
            'max': max_cooldown,
            'current': 0
        }
    
    def update(self, dt):
        """Update cooldowns for all events"""
        for event in self.event_cooldowns.values():
            if event['current'] > 0:
                event['current'] -= dt
    
    def trigger_event(self, event_name, probability=0.5):
        """
        Try to trigger an event based on quantum probability
        Returns True if event triggered, False otherwise
        """
        if event_name not in self.event_cooldowns:
            return False
            
        event = self.event_cooldowns[event_name]
        
        # Check if event is on cooldown
        if event['current'] > 0:
            return False
        
        # Use quantum randomness to determine if event triggers
        if self.quantum_sim.get_quantum_random() < probability:
            # Event triggered, set cooldown
            cooldown = self.quantum_sim.get_quantum_random(event['min'], event['max'])
            event['current'] = cooldown
            
            # Record event
            self.event_history.append({
                'name': event_name,
                'time': pygame.time.get_ticks() if 'pygame' in sys.modules else 0
            })
            
            return True
        
        return False
    
    def get_event_probability(self, event_name, base_probability=0.5):
        """Get quantum-adjusted probability for an event"""
        # Analyze event history to adjust probability
        recent_events = [e for e in self.event_history[-10:] if e['name'] == event_name]
        history_factor = len(recent_events) / 10 if recent_events else 0
        
        # Use quantum simulation to adjust probability
        quantum_factor = self.quantum_sim.get_quantum_random(-0.2, 0.2)
        
        # Calculate final probability
        adjusted_prob = base_probability - history_factor * 0.3 + quantum_factor
        
        # Ensure probability is in valid range
        return max(0.05, min(0.95, adjusted_prob))

# Quantum AI decision making for enemies
class QuantumDecisionMaker:
    def __init__(self, num_qubits=3):
        self.quantum_sim = QuantumSimulator(num_qubits)
        self.decision_history = []
        self.personality = {
            'aggression': random.random(),
            'caution': random.random(),
            'unpredictability': random.random()
        }
    
    def make_decision(self, options, context=None):
        """
        Make a decision based on quantum principles and context
        options: list of possible decisions
        context: optional dict with contextual information
        """
        if not options:
            return None
            
        # Default equal weights
        weights = [1.0] * len(options)
        
        # Adjust weights based on context and personality
        if context:
            for i, option in enumerate(options):
                # Adjust for player proximity if that info is available
                if 'player_distance' in context:
                    if option == 'attack' or option == 'chase':
                        # More likely to attack when player is close
                        proximity_factor = 1.0 - min(1.0, context['player_distance'] / 300)
                        weights[i] *= 1.0 + proximity_factor * self.personality['aggression']
                    elif option == 'flee' or option == 'defend':
                        # More likely to flee when player is close
                        proximity_factor = 1.0 - min(1.0, context['player_distance'] / 200)
                        weights[i] *= 1.0 + proximity_factor * self.personality['caution']
                
                # Adjust for health if that info is available
                if 'health_percent' in context:
                    if option == 'attack':
                        # Less likely to attack when low health
                        weights[i] *= context['health_percent'] * (2 - self.personality['caution'])
                    elif option == 'flee':
                        # More likely to flee when low health
                        weights[i] *= (1.0 + (1.0 - context['health_percent']) * 2 * self.personality['caution'])
        
        # Add quantum unpredictability based on personality
        for i in range(len(weights)):
            quantum_factor = self.quantum_sim.get_quantum_random(-0.5, 0.5)
            weights[i] *= 1.0 + quantum_factor * self.personality['unpredictability']
            weights[i] = max(0.1, weights[i])  # Ensure positive weight
        
        # Make the quantum decision
        decision = self.quantum_sim.get_quantum_decision(options, weights)
        
        # Record the decision
        self.decision_history.append({
            'decision': decision,
            'context': context,
            'time': pygame.time.get_ticks() if 'pygame' in sys.modules else 0
        })
        
        return decision
    
    def analyze_history(self):
        """Analyze decision history to evolve personality"""
        if len(self.decision_history) < 10:
            return
            
        # Count decision types
        decision_counts = {}
        for entry in self.decision_history[-20:]:
            decision = entry['decision']
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        # Adjust personality based on decisions
        if 'attack' in decision_counts and 'flee' in decision_counts:
            attack_ratio = decision_counts['attack'] / (decision_counts['attack'] + decision_counts['flee'])
            # Gradually shift personality
            self.personality['aggression'] = 0.8 * self.personality['aggression'] + 0.2 * attack_ratio
            self.personality['caution'] = 0.8 * self.personality['caution'] + 0.2 * (1.0 - attack_ratio)
        
        # Add some quantum randomness to personality evolution
        for trait in self.personality:
            quantum_shift = self.quantum_sim.get_quantum_random(-0.1, 0.1)
            self.personality[trait] = max(0.1, min(0.9, self.personality[trait] + quantum_shift))

# Import necessary modules
import sys
if 'pygame' in sys.modules:
    import pygame