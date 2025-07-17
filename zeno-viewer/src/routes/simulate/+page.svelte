<script lang="ts">
	export let data;
	async function runSim() {
		await fetch("http://localhost:9000/simulate", {
			method: "POST"
		});
	}
</script>

<h1>Simulation Viewer</h1>

<button on:click={runSim}>Start Simulation</button>

<p>Status: {data.status}</p>
{#if data.metrics}
	<p><a href={"http://localhost:9000/" + data.metrics} target="_blank">View Metrics</a></p>
{/if}
