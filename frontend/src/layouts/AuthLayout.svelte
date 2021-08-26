<script lang="ts">
  import RootLayout from "./RootLayout.svelte";
</script>

<style>
  .wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
  }

  .card {
    padding: var(--gap-md);
    background-color: var(--dark-gray);
    border-radius: 4px;
    width: 400px;
  }
</style>

<RootLayout>
  <div class="wrapper">
    <div class="card">
      <slot />
    </div>
  </div>
</RootLayout>
