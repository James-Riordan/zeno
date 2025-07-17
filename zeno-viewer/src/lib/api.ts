// src/lib/api.ts

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:9000";

export type SimParams = {
	dim: number;
	grid: number;
	steps: number;
	scene: string;
	mode: "symbolic" | "classical";
};

export type SimStatus =
	| { status: "running"; output_dir: string }
	| { status: "done"; path: string; timestamp: string }
	| { status: "unknown"; message: string };

export async function startSimulation(params: SimParams): Promise<{ status: string }> {
	const res = await fetch(`${API_BASE}/simulate`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(params)
	});

	if (!res.ok) {
		const errorText = await res.text();
		throw new Error(`Simulation failed: ${errorText}`);
	}

	return res.json();
}

export async function getSimStatus(scene: string): Promise<SimStatus> {
	const res = await fetch(`${API_BASE}/status?scene=${scene}`);
	if (!res.ok) {
		const errorText = await res.text();
		throw new Error(`Status fetch failed: ${errorText}`);
	}
	return res.json();
}
