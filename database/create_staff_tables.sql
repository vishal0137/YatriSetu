-- Create Drivers Table
CREATE TABLE IF NOT EXISTS drivers (
    id SERIAL PRIMARY KEY,
    driver_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_expiry DATE,
    date_of_birth DATE,
    address TEXT,
    experience_years INTEGER,
    assigned_bus_id INTEGER REFERENCES buses(id),
    assigned_route_id INTEGER REFERENCES routes(id),
    shift VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Active',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create Conductors Table
CREATE TABLE IF NOT EXISTS conductors (
    id SERIAL PRIMARY KEY,
    conductor_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    date_of_birth DATE,
    address TEXT,
    experience_years INTEGER,
    assigned_bus_id INTEGER REFERENCES buses(id),
    assigned_route_id INTEGER REFERENCES routes(id),
    shift VARCHAR(20),
    role VARCHAR(50) DEFAULT 'Conductor',
    status VARCHAR(20) DEFAULT 'Active',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_drivers_status ON drivers(status);
CREATE INDEX IF NOT EXISTS idx_drivers_shift ON drivers(shift);
CREATE INDEX IF NOT EXISTS idx_drivers_assigned_bus ON drivers(assigned_bus_id);
CREATE INDEX IF NOT EXISTS idx_drivers_assigned_route ON drivers(assigned_route_id);

CREATE INDEX IF NOT EXISTS idx_conductors_status ON conductors(status);
CREATE INDEX IF NOT EXISTS idx_conductors_shift ON conductors(shift);
CREATE INDEX IF NOT EXISTS idx_conductors_assigned_bus ON conductors(assigned_bus_id);
CREATE INDEX IF NOT EXISTS idx_conductors_assigned_route ON conductors(assigned_route_id);
CREATE INDEX IF NOT EXISTS idx_conductors_role ON conductors(role);
