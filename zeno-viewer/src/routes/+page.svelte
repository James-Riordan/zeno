<script lang="ts">
	import { onMount } from 'svelte';
	import { startSimulation, getSimStatus, type SimStatus } from '$lib/api';

	let dim = 2;
	let grid = 128;
	let steps = 500;
	let scene = 'RTI_2D';
	let mode: 'symbolic' | 'classical' = 'symbolic';

	let isSubmitting = false;
	let status: SimStatus | null = null;
	let error: string | null = null;

	async function runSimulation() {
		error = null;
		status = null;
		isSubmitting = true;

		try {
			await startSimulation({ dim, grid, steps, scene, mode });
			await pollStatus();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Unknown error';
		} finally {
			isSubmitting = false;
		}
	}

	async function pollStatus(retries = 30, delay = 2000) {
		for (let i = 0; i < retries; i++) {
			try {
				const res = await getSimStatus(scene);
				status = res;

				if (res.status === 'done' || res.status === 'unknown') {
					return;
				}
			} catch (err) {
				error = 'Failed to poll status';
				break;
			}

			await new Promise(r => setTimeout(r, delay));
		}
	}
</script>

<style>
	label {
		font-weight: 600;
	}
</style>

<h1 class="text-2xl font-bold mb-4">Zeno Engine Simulation</h1>

<div class="grid grid-cols-2 gap-4 mb-6">
	<div>
		<label for="scene">Scene:</label>
		<input id="scene" bind:value={scene} class="w-full p-2 border rounded" />
	</div>

	<div>
		<label for="dim">Dimension:</label>
		<select id="dim" bind:value={dim} class="w-full p-2 border rounded">
			<option value="1">1D</option>
			<option value="2">2D</option>
			<option value="3">3D</option>
		</select>
	</div>

	<div>
		<label for="grid">Grid Size:</label>
		<input id="grid" type="number" bind:value={grid} min="8" max="512" class="w-full p-2 border rounded" />
	</div>

	<div>
		<label for="steps">Steps:</label>
		<input id="steps" type="number" bind:value={steps} min="1" max="10000" class="w-full p-2 border rounded" />
	</div>

	<div>
		<label for="mode">Mode:</label>
		<select id="mode" bind:value={mode} class="w-full p-2 border rounded">
			<option value="symbolic">Symbolic</option>
			<option value="classical">Classical</option>
		</select>
	</div>
</div>

<button
	class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
	on:click={runSimulation}
	disabled={isSubmitting}
>
	{isSubmitting ? 'Running...' : 'Run Simulation'}
</button>

{#if error}
	<p class="mt-4 text-red-500">❌ {error}</p>
{/if}

{#if status}
	<div class="mt-6 p-4 bg-gray-100 border rounded">
		<h2 class="font-bold mb-2">Status</h2>
		<pre class="text-sm">{JSON.stringify(status, null, 2)}</pre>
	</div>
{/if}

{#if status?.status === 'done'}
	<div class="mt-6">
		<h2 class="font-bold mb-2">📈 Output Preview</h2>
		<!-- Placeholder for rendering output (e.g. image, video, 3D scene) -->
		<div class="w-full h-[300px] bg-black text-white flex items-center justify-center">
			Canvas placeholder (to be replaced with Three.js)
		</div>
	</div>
{/if}
