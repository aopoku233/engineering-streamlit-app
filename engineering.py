"""
Engineering calculations module for the Streamlit multi-page app.
Contains OOP classes for fluid properties, pipe flow, and heat transfer.
All methods include docstrings and basic error handling.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np
import math


@dataclass
class Fluid:
    """
    Represents a fluid with its physical properties.
    
    Attributes:
        name (str): Name of the fluid.
        density (float): Density in kg/m³.
        viscosity (float): Dynamic viscosity in Pa·s (N·s/m²).
        specific_heat (float): Specific heat capacity in J/(kg·K). Optional for flow calcs.
    """
    name: str
    density: float  # kg/m³
    viscosity: float  # Pa·s
    specific_heat: Optional[float] = None  # J/(kg·K)

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be positive.")
        if self.viscosity <= 0:
            raise ValueError("Viscosity must be positive.")

    @classmethod
    def water(cls, temperature_c: float = 20.0) -> "Fluid":
        """Factory for water properties at approximately given temperature (°C)."""
        # Approximate values around 20°C
        return cls(name="Water", density=998.0, viscosity=1.002e-3, specific_heat=4182.0)

    @classmethod
    def air(cls, temperature_c: float = 20.0) -> "Fluid":
        """Factory for dry air at approx 20°C, 1 atm."""
        return cls(name="Air", density=1.204, viscosity=1.825e-5, specific_heat=1006.0)

    @classmethod
    def crude_oil(cls) -> "Fluid":
        """Typical medium crude oil properties (approx)."""
        return cls(name="Crude Oil", density=850.0, viscosity=0.01, specific_heat=1900.0)

    @classmethod
    def custom(cls, name: str, density: float, viscosity: float, specific_heat: float = 2000.0) -> "Fluid":
        """Create a user-defined fluid."""
        return cls(name=name, density=density, viscosity=viscosity, specific_heat=specific_heat)


class Pipe:
    """
    Models a circular pipe for steady incompressible flow analysis
    using Darcy-Weisbach equation.
    """

    def __init__(self, diameter: float, length: float, roughness: float):
        """
        Initialize pipe geometry.
        
        Args:
            diameter (float): Internal diameter in meters. Must be > 0.
            length (float): Pipe length in meters. Must be > 0.
            roughness (float): Absolute roughness ε in meters. Must be >= 0.
        """
        if diameter <= 0:
            raise ValueError("Pipe diameter must be positive.")
        if length <= 0:
            raise ValueError("Pipe length must be positive.")
        if roughness < 0:
            raise ValueError("Roughness cannot be negative.")
        self.diameter = diameter  # m
        self.length = length  # m
        self.roughness = roughness  # m
        self.area = math.pi * (diameter / 2) ** 2  # m²

    def reynolds_number(self, velocity: float, fluid: Fluid) -> float:
        """
        Calculate Reynolds number Re = ρ V D / μ.
        
        Args:
            velocity (float): Mean velocity in m/s.
            fluid (Fluid): Fluid object.
            
        Returns:
            float: Reynolds number (dimensionless).
        """
        if velocity < 0:
            raise ValueError("Velocity cannot be negative.")
        return (fluid.density * velocity * self.diameter) / fluid.viscosity

    def friction_factor(self, re: float) -> float:
        """
        Calculate Darcy friction factor.
        - Laminar (Re < 2300): f = 64 / Re
        - Turbulent: Haaland explicit approximation to Colebrook-White.
        
        Args:
            re (float): Reynolds number.
            
        Returns:
            float: Darcy friction factor f.
        """
        if re <= 0:
            raise ValueError("Reynolds number must be positive.")
        if re < 2300:
            return 64.0 / re
        # Haaland approximation (good accuracy for engineering)
        rel_rough = self.roughness / self.diameter
        term1 = (rel_rough / 3.7) ** 1.11
        term2 = 6.9 / re
        inv_sqrt_f = -1.8 * math.log10(term1 + term2)
        return 1.0 / (inv_sqrt_f ** 2)

    def velocity_from_flowrate(self, q: float) -> float:
        """
        Mean velocity from volumetric flow rate.
        
        Args:
            q (float): Volumetric flow rate in m³/s.
            
        Returns:
            float: Velocity in m/s.
        """
        if q < 0:
            raise ValueError("Flow rate cannot be negative.")
        return q / self.area

    def pressure_drop(self, q: float, fluid: Fluid) -> Tuple[float, float, float, float]:
        """
        Compute velocity, Re, friction factor and pressure drop (Darcy-Weisbach).
        
        ΔP = f * (L/D) * (ρ V² / 2)
        
        Args:
            q (float): Flow rate in m³/s.
            fluid (Fluid): Fluid object.
            
        Returns:
            Tuple[float, float, float, float]: (velocity, Re, f, ΔP in Pa)
        """
        v = self.velocity_from_flowrate(q)
        re = self.reynolds_number(v, fluid)
        f = self.friction_factor(re)
        dp = f * (self.length / self.diameter) * (fluid.density * v ** 2 / 2.0)
        return v, re, f, dp

    def pressure_drop_vs_flowrate(self, q_min: float, q_max: float, fluid: Fluid, n_points: int = 50) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate arrays of flow rate and corresponding pressure drop for plotting.
        
        Args:
            q_min, q_max (float): Range of flow rates (m³/s).
            fluid (Fluid): Fluid.
            n_points (int): Number of points.
            
        Returns:
            Tuple of (q_array, dp_array)
        """
        qs = np.linspace(q_min, q_max, n_points)
        dps = np.array([self.pressure_drop(q, fluid)[3] for q in qs])
        return qs, dps


class HeatTransfer:
    """
    Utility class for simple heat transfer calculations:
    1. Steady 1D conduction through a flat wall (Fourier's law).
    2. Transient cooling via Newton's Law of Cooling.
    """

    @staticmethod
    def conduction_flat_wall(k: float, area: float, thickness: float, t_hot: float, t_cold: float) -> float:
        """
        Steady-state heat transfer rate through a single-layer flat wall.
        Q = k * A * (T_hot - T_cold) / L   (Fourier's law)
        
        Args:
            k (float): Thermal conductivity in W/(m·K).
            area (float): Cross-sectional area perpendicular to heat flow (m²).
            thickness (float): Wall thickness L (m).
            t_hot (float): Hot side temperature (°C or K, consistent).
            t_cold (float): Cold side temperature.
            
        Returns:
            float: Heat transfer rate Q in Watts.
        """
        if k <= 0 or area <= 0 or thickness <= 0:
            raise ValueError("k, area and thickness must be positive.")
        return k * area * (t_hot - t_cold) / thickness

    @staticmethod
    def newtons_cooling_time(
        t0: float,
        t_target: float,
        t_inf: float,
        h: float,
        area: float,
        mass: float,
        cp: float
    ) -> float:
        """
        Time required for an object to cool (or heat) from T0 to T_target
        in ambient temperature T_inf according to Newton's Law of Cooling.
        
        T(t) = T_inf + (T0 - T_inf) * exp( - (h A)/(m cp) * t )
        
        Solved for t:
        t = [m cp / (h A)] * ln( (T0 - T_inf) / (T_target - T_inf) )
        
        Args:
            t0 (float): Initial temperature (°C).
            t_target (float): Target temperature (°C).
            t_inf (float): Ambient fluid temperature (°C).
            h (float): Convective heat transfer coefficient (W/(m²·K)).
            area (float): Surface area exposed to convection (m²).
            mass (float): Mass of the object (kg).
            cp (float): Specific heat capacity (J/(kg·K)).
            
        Returns:
            float: Time in seconds. Raises ValueError if physically impossible.
        """
        if h <= 0 or area <= 0 or mass <= 0 or cp <= 0:
            raise ValueError("h, area, mass and cp must be positive.")
        
        # Check direction and possibility
        if abs(t0 - t_inf) < 1e-9:
            raise ValueError("Initial temperature equals ambient; no temperature change occurs.")
        
        # For cooling (t0 > t_inf), target must be between t_inf and t0
        # For heating (t0 < t_inf), target between t0 and t_inf
        if (t0 > t_inf and not (t_inf < t_target < t0)) or \
           (t0 < t_inf and not (t0 < t_target < t_inf)):
            raise ValueError(
                "Target temperature is not reachable under Newton's law "
                "(must lie strictly between T0 and T_inf)."
            )
        
        tau = (mass * cp) / (h * area)  # time constant
        ratio = (t0 - t_inf) / (t_target - t_inf)
        t = tau * math.log(ratio)
        return t

    @staticmethod
    def temperature_history(
        t0: float,
        t_inf: float,
        h: float,
        area: float,
        mass: float,
        cp: float,
        t_max: float,
        n_points: int = 200
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate temperature vs time arrays for plotting the cooling/heating curve.
        
        Args:
            ... (same physical parameters)
            t_max (float): Maximum time to simulate (s).
            n_points (int): Number of points.
            
        Returns:
            (time_array, temperature_array)
        """
        times = np.linspace(0, t_max, n_points)
        tau = (mass * cp) / (h * area)
        temps = t_inf + (t0 - t_inf) * np.exp(-times / tau)
        return times, temps
