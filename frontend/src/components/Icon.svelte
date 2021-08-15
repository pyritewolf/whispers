<script lang="ts">
  import { onMount } from "svelte";
  import { Gap, Color, BrandIcon } from "../types/components";
  import type { IconName } from "../types/components";
  export let name: IconName;
  export let size: Gap = Gap.md;
  export let color: Color = Color.white;

  let lineAwesomeClass: string = "las";

  onMount(() => {
    if ((<any>Object).values(BrandIcon).includes(name))
      lineAwesomeClass = "lab";
  });
</script>

<style>
  .icon {
    font-size: var(--size);
    line-height: 1;
    color: var(--color);
  }
</style>

<i
  class="icon {lineAwesomeClass} la-{name}"
  style="--size: var({size}); --color: var({color})" />
