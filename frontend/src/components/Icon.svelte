<script lang="ts">
  import { Gap, Color, IconName } from "../types/components";
  export let name: IconName;
  export let size: Gap = Gap.md;
  export let color: Color = Color.white;
</script>

<style>
  .icon {
    font-size: var(--size);
    line-height: 1;
    color: var(--color);
  }
</style>

<i
  class="icon las la-{name}"
  style="--size: var({size}); --color: var({color})" />
