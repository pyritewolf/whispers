<script lang="ts">
</script>

<div class="wrapper">
  <div class="card">
    <slot/>
  </div>
</div>

<style>
  .wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .card {
    padding: var(--gap-md);
    background-color: var(--dark-gray);
    border-radius: 4px;
    width: 400px;
  }
</style>
