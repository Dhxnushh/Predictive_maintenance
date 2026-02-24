"""
Real-time Data Simulator for Predictive Maintenance System
Simulates realistic sensor data for multiple machines
"""
import numpy as np
import random
import time
import config
from datetime import datetime
import json


class MachineSimulator:
    """
    Simulates sensor data for a single machine
    """
    
    def __init__(self, machine_id, machine_type=None, initial_condition='healthy'):
        self.machine_id = machine_id
        self.machine_type = machine_type or random.choice(config.SENSOR_RANGES['Type'])
        
        # Set initial tool wear and sensor baselines based on condition
        if initial_condition == 'healthy':
            # Healthy condition: low wear, optimal sensor values
            self.tool_wear = random.uniform(5, 45)
            self.air_temp_baseline = random.uniform(296, 299.5)  # Lower, optimal range
            self.process_temp_baseline = random.uniform(306, 309.5)  # Lower, optimal range
            self.speed_baseline = random.uniform(1600, 2100)  # Higher speed
            self.torque_baseline = random.uniform(22, 38)  # Lower torque
            self.degradation_rate = random.uniform(0.15, 0.3)  # Very slow
        elif initial_condition == 'risk':
            # At risk: approaching maintenance threshold (30-60% failure probability)
            # Need values very similar to maintenance but slightly better
            self.tool_wear = random.uniform(165, 185)  # High wear, approaching maintenance
            self.air_temp_baseline = random.uniform(301, 303)  # Elevated
            self.process_temp_baseline = random.uniform(311.2, 312.8)  # High
            self.speed_baseline = random.uniform(1240, 1300)  # Low speed
            self.torque_baseline = random.uniform(63, 68)  # Very high torque
            self.degradation_rate = random.uniform(0.2, 0.35)  # Controlled
        elif initial_condition == 'maintenance':
            # Maintenance required: high wear, clearly degraded sensor values
            self.tool_wear = random.uniform(180, 220)  # Very high wear
            self.air_temp_baseline = random.uniform(301, 303.5)  # Elevated
            self.process_temp_baseline = random.uniform(311, 313)  # Very high
            self.speed_baseline = random.uniform(1220, 1320)  # Low speed
            self.torque_baseline = random.uniform(62, 70)  # Very high torque
            self.degradation_rate = random.uniform(0.2, 0.35)  # Controlled
        else:
            # Default to healthy
            self.tool_wear = random.uniform(5, 40)
            self.air_temp_baseline = random.uniform(296, 300)
            self.process_temp_baseline = random.uniform(306, 310)
            self.speed_baseline = random.uniform(1500, 2000)
            self.torque_baseline = random.uniform(25, 40)
            self.degradation_rate = random.uniform(0.2, 0.4)
        
        # Operating mode
        self.operating_mode = "normal"
        self.cycles = 0
        
    def generate_sensor_data(self):
        """
        Generate realistic sensor data with correlations and gradual degradation
        """
        self.cycles += 1
        
        # GRADUAL tool wear increase (much slower, realistic)
        wear_increment = self.degradation_rate * random.uniform(0.1, 0.3)  # Very small increments
        self.tool_wear = min(self.tool_wear + wear_increment, 250)
        
        # Generate correlated sensor readings with minimal noise for gradual changes
        # Air temperature - very slow variations
        air_temp_noise = random.gauss(0, 0.2)  # Reduced noise
        air_temp = np.clip(
            self.air_temp_baseline + air_temp_noise,
            *config.SENSOR_RANGES['Air temperature [K]']
        )
        
        # Process temperature - correlated with air temp, slightly increases with tool wear
        wear_factor = self.tool_wear / 250.0  # 0 to 1
        process_temp_base = air_temp + random.uniform(8, 12)
        process_temp_noise = random.gauss(0, 0.3) + wear_factor * 1.0  # Reduced impact
        process_temp = np.clip(
            process_temp_base + process_temp_noise,
            *config.SENSOR_RANGES['Process temperature [K]']
        )
        
        # Rotational speed - very stable with minor variations
        speed_noise = random.gauss(0, 20)  # Reduced from 50
        speed = np.clip(
            self.speed_baseline + speed_noise,
            *config.SENSOR_RANGES['Rotational speed [rpm]']
        )
        
        # Torque - stable with slight variations based on wear
        base_torque = self.torque_baseline
        if wear_factor > 0.6:  # High wear increases torque slightly
            base_torque += random.uniform(0, 3)  # Reduced from 10
        
        torque_noise = random.gauss(0, 1.5)  # Reduced from 3
        torque = np.clip(
            base_torque + torque_noise,
            *config.SENSOR_RANGES['Torque [Nm]']
        )
        
        # Very gradual baseline drift (simulate aging over many cycles)
        if self.cycles % 100 == 0:
            self.air_temp_baseline += random.uniform(-0.1, 0.1)
            self.speed_baseline += random.uniform(-5, 5)
            self.torque_baseline += random.uniform(-0.5, 0.5)
        
        return {
            'machine_id': self.machine_id,
            'Type': self.machine_type,
            'Air temperature [K]': round(air_temp, 1),
            'Process temperature [K]': round(process_temp, 1),
            'Rotational speed [rpm]': int(speed),
            'Torque [Nm]': round(torque, 1),
            'Tool wear [min]': int(self.tool_wear),
            'timestamp': datetime.now().isoformat(),
            'operating_mode': self.operating_mode,
            'cycles': self.cycles
        }
    
    def reset_tool_wear(self):
        """Simulate maintenance - reset tool wear to healthy state"""
        self.tool_wear = random.uniform(0, 20)  # Fresh after maintenance
        self.degradation_rate = random.uniform(0.2, 0.5)  # Reset to slow degradation
        print(f"  🔧 Maintenance performed on {self.machine_id} - Tool wear reset to {int(self.tool_wear)}min")


class DataSimulator:
    """
    Manages multiple machine simulators
    """
    
    def __init__(self, num_machines=None):
        self.num_machines = num_machines or config.NUM_MACHINES
        self.machines = []
        
        # Define initial conditions for machines
        # 3 healthy, 1 at risk, 1 requiring maintenance
        conditions = ['healthy', 'healthy', 'healthy', 'risk', 'maintenance']
        
        # Ensure we have enough conditions
        while len(conditions) < self.num_machines:
            conditions.append('healthy')
        
        # Initialize machines with specific conditions
        for i in range(self.num_machines):
            machine_id = f"M{str(i+1).zfill(3)}"
            machine_type = random.choice(config.SENSOR_RANGES['Type'])
            condition = conditions[i] if i < len(conditions) else 'healthy'
            machine = MachineSimulator(machine_id, machine_type, initial_condition=condition)
            self.machines.append(machine)
        
        print(f"✓ Initialized {self.num_machines} machine simulators")
        for machine in self.machines:
            status = "HEALTHY" if machine.tool_wear < 50 else ("AT RISK" if machine.tool_wear < 150 else "MAINTENANCE")
            print(f"  - {machine.machine_id} (Type: {machine.machine_type}, Tool Wear: {int(machine.tool_wear)}min, Status: {status})")

    
    def generate_data(self, machine_id=None):
        """
        Generate sensor data for one or all machines
        """
        if machine_id:
            machine = next((m for m in self.machines if m.machine_id == machine_id), None)
            if machine:
                return machine.generate_sensor_data()
            else:
                raise ValueError(f"Machine {machine_id} not found")
        else:
            return [machine.generate_sensor_data() for machine in self.machines]
    
    def perform_maintenance(self, machine_id):
        """
        Perform maintenance on a specific machine
        """
        machine = next((m for m in self.machines if m.machine_id == machine_id), None)
        if machine:
            machine.reset_tool_wear()
            return True
        return False
    
    def get_machines_info(self):
        """
        Get information about all machines
        """
        return [{
            'machine_id': m.machine_id,
            'type': m.machine_type,
            'tool_wear': int(m.tool_wear),
            'operating_mode': m.operating_mode,
            'cycles': m.cycles,
            'degradation_rate': round(m.degradation_rate, 2)
        } for m in self.machines]
    
    def run_continuous_simulation(self, callback=None, interval=None):
        """
        Run continuous simulation loop
        
        Args:
            callback: Function to call with generated data
            interval: Time interval between generations (seconds)
        """
        interval = interval or config.SIMULATION_INTERVAL
        
        print(f"\n{'='*60}")
        print("STARTING CONTINUOUS SIMULATION")
        print(f"{'='*60}")
        print(f"Interval: {interval} seconds")
        print(f"Machines: {self.num_machines}")
        print("Press Ctrl+C to stop\n")
        
        try:
            iteration = 0
            while True:
                iteration += 1
                
                # Generate data for all machines
                data = self.generate_data()
                
                # Display summary
                print(f"\n[Iteration {iteration}] {datetime.now().strftime('%H:%M:%S')}")
                for machine_data in data:
                    print(f"  {machine_data['machine_id']}: "
                          f"Temp={machine_data['Process temperature [K]']:.1f}K, "
                          f"Speed={machine_data['Rotational speed [rpm]']}rpm, "
                          f"Torque={machine_data['Torque [Nm]']:.1f}Nm, "
                          f"Wear={machine_data['Tool wear [min]']}min")
                
                # Call callback if provided
                if callback:
                    callback(data)
                
                # Wait for next iteration
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n✓ Simulation stopped by user")


# Create global simulator instance
_simulator = None

def get_simulator():
    """Get or create simulator singleton"""
    global _simulator
    if _simulator is None:
        _simulator = DataSimulator()
    return _simulator


if __name__ == "__main__":
    # Test the simulator
    simulator = DataSimulator(num_machines=3)
    
    print("\nGenerating sample data...")
    data = simulator.generate_data()
    
    print("\nSample output:")
    print(json.dumps(data, indent=2))
    
    print("\n" + "="*60)
    print("Starting continuous simulation (5 iterations)...")
    print("="*60)
    
    for i in range(5):
        data = simulator.generate_data()
        print(f"\n[Iteration {i+1}]")
        for machine_data in data:
            print(f"  {machine_data['machine_id']}: Wear={machine_data['Tool wear [min]']}min")
        time.sleep(1)
    
    print("\n✓ Simulation test completed")
