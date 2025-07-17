export async function load({ fetch }) {
	const response = await fetch("http://localhost:9000/status?scene=RTI_2D");
	const data = await response.json();

	return {
		status: data.status,
		message: data.message ?? null,
		metrics: data.path ?? null
	};
}
