//! Newton-Raphson root finding algorithm
//!
//! Implements iterative root finding for continuous functions

use std::fmt;

/// Error types for Newton-Raphson solver
#[derive(Debug, Clone, PartialEq)]
pub enum NewtonRaphsonError {
    /// Maximum iterations reached without convergence
    MaxIterationsReached { iterations: usize, last_value: f64 },
    /// Derivative is zero or near-zero, preventing progress
    ZeroDerivative { x: f64 },
    /// Solution diverged (value became NaN or infinite)
    Diverged,
}

impl fmt::Display for NewtonRaphsonError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::MaxIterationsReached {
                iterations,
                last_value,
            } => {
                write!(
                    f,
                    "Maximum iterations ({}) reached at x = {}",
                    iterations, last_value
                )
            }
            Self::ZeroDerivative { x } => {
                write!(f, "Derivative is zero at x = {}", x)
            }
            Self::Diverged => {
                write!(f, "Solution diverged (NaN or infinite)")
            }
        }
    }
}

impl std::error::Error for NewtonRaphsonError {}

pub type Result<T> = std::result::Result<T, NewtonRaphsonError>;

/// Newton-Raphson solver configuration
pub struct NewtonRaphsonSolver {
    /// Maximum number of iterations
    pub max_iterations: usize,
    /// Convergence tolerance (absolute difference)
    pub tolerance: f64,
    /// Minimum acceptable derivative value
    pub min_derivative: f64,
}

impl Default for NewtonRaphsonSolver {
    fn default() -> Self {
        Self {
            max_iterations: 50,
            tolerance: 1e-10,
            min_derivative: 1e-15,
        }
    }
}

impl NewtonRaphsonSolver {
    /// Create a new solver with custom parameters
    pub fn new(max_iterations: usize, tolerance: f64) -> Self {
        Self {
            max_iterations,
            tolerance,
            min_derivative: 1e-15,
        }
    }

    /// Find root of f(x) = 0 using Newton-Raphson method
    pub fn solve<F, DF>(&self, f: &F, df: &DF, initial_guess: f64) -> Result<f64>
    where
        F: Fn(f64) -> f64,
        DF: Fn(f64) -> f64,
    {
        let mut x = initial_guess;

        for _iteration in 0..self.max_iterations {
            let fx = f(x);

            // Check for convergence
            if fx.abs() < self.tolerance {
                return Ok(x);
            }

            // Check for divergence
            if !fx.is_finite() {
                return Err(NewtonRaphsonError::Diverged);
            }

            let dfx = df(x);

            // Check if derivative is too small
            if dfx.abs() < self.min_derivative {
                return Err(NewtonRaphsonError::ZeroDerivative { x });
            }

            // Newton-Raphson iteration
            x = x - fx / dfx;

            // Check if new x is valid
            if !x.is_finite() {
                return Err(NewtonRaphsonError::Diverged);
            }
        }

        Err(NewtonRaphsonError::MaxIterationsReached {
            iterations: self.max_iterations,
            last_value: x,
        })
    }

    /// Find root using numerical derivative approximation
    pub fn solve_numerical<F>(&self, f: F, initial_guess: f64, h: f64) -> Result<f64>
    where
        F: Fn(f64) -> f64,
    {
        let df = |x: f64| (f(x + h) - f(x - h)) / (2.0 * h);
        self.solve(&f, &df, initial_guess)
    }

    /// Find root for periodic functions (handles angle wrapping)
    pub fn solve_periodic<F, DF>(
        &self,
        f: F,
        df: DF,
        initial_guess: f64,
        period: f64,
    ) -> Result<f64>
    where
        F: Fn(f64) -> f64,
        DF: Fn(f64) -> f64,
    {
        let wrapped_f = |x: f64| {
            let val = f(x);
            // Normalize to [-period/2, period/2]
            let normalized = val % period;
            if normalized > period / 2.0 {
                normalized - period
            } else if normalized < -period / 2.0 {
                normalized + period
            } else {
                normalized
            }
        };

        self.solve(&wrapped_f, &df, initial_guess)
    }
}

/// Convenience function for simple root finding
pub fn find_root<F, DF>(f: F, df: DF, initial_guess: f64) -> Result<f64>
where
    F: Fn(f64) -> f64,
    DF: Fn(f64) -> f64,
{
    NewtonRaphsonSolver::default().solve(&f, &df, initial_guess)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_quadratic() {
        // Solve x^2 - 4 = 0, expect x = 2
        let f = |x: f64| x * x - 4.0;
        let df = |x: f64| 2.0 * x;

        let result = find_root(f, df, 1.0).unwrap();
        assert!((result - 2.0).abs() < 1e-9);
    }

    #[test]
    fn test_cubic() {
        // Solve x^3 - x - 2 = 0, expect x ≈ 1.521
        let f = |x: f64| x.powi(3) - x - 2.0;
        let df = |x: f64| 3.0 * x.powi(2) - 1.0;

        let result = find_root(f, df, 2.0).unwrap();
        assert!((result - 1.5213797).abs() < 1e-6);
    }

    #[test]
    fn test_transcendental() {
        // Solve cos(x) - x = 0, expect x ≈ 0.739
        let f = |x: f64| x.cos() - x;
        let df = |x: f64| -x.sin() - 1.0;

        let result = find_root(f, df, 0.5).unwrap();
        assert!((result - 0.7390851).abs() < 1e-6);
    }

    #[test]
    fn test_numerical_derivative() {
        // Solve x^2 - 9 = 0 using numerical derivative
        let f = |x: f64| x * x - 9.0;

        let solver = NewtonRaphsonSolver::default();
        let result = solver.solve_numerical(f, 2.0, 0.001).unwrap();
        assert!((result - 3.0).abs() < 1e-6);
    }

    #[test]
    fn test_periodic_function() {
        // Solve sin(x) = 0.5, expect x ≈ 30° (π/6 radians = 0.5236)
        let f = |x: f64| x.to_radians().sin() - 0.5;
        let df = |x: f64| x.to_radians().cos() * std::f64::consts::PI / 180.0;

        let solver = NewtonRaphsonSolver::default();
        let result = solver.solve_periodic(f, df, 25.0, 360.0).unwrap();
        assert!((result - 30.0).abs() < 1e-6);
    }

    #[test]
    fn test_max_iterations() {
        // Function that won't converge (derivative → 0)
        let f = |x: f64| x.abs().sqrt();
        let df = |x: f64| 0.5 / x.abs().sqrt();

        let result = find_root(f, df, 1.0);
        assert!(matches!(
            result,
            Err(NewtonRaphsonError::MaxIterationsReached { .. })
        ));
    }

    #[test]
    fn test_zero_derivative() {
        // Function with zero derivative at a point
        let f = |x: f64| (x - 1.0).powi(2);
        let df = |_x: f64| 0.0; // Force zero derivative

        let result = find_root(f, df, 2.0);
        assert!(matches!(
            result,
            Err(NewtonRaphsonError::ZeroDerivative { .. })
        ));
    }
}
