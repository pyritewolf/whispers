<script lang="ts">
  import { ButtonType, Size, Color } from "../types/components";

  export let type: ButtonType = ButtonType.submit;
  export let color: Color = Color.gray;
  export let textColor: Color = Color.white;
  export let size: Size = Size.md;
  export let disabled: boolean = false;
  export let click = () => {};

  let focused: boolean = false;
</script>

<style>
  button {
    background-color: var(--color);
    border-radius: var(--radius);
    padding: var(--gap-md);
    color: var(--text-color);
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--gap-sm);
    border-radius: var(--radius);
    text-align: center;
    cursor: pointer;
    text-transform: uppercase;
    transition: var(--transition);
  }

  button:hover,
  button:focus {
    filter: brightness(0.85);
    transition: var(--transition);
  }

  button.small {
    padding: var(--gap-sm);
    font-size: var(--font-sm);
  }

  button.large {
    padding: var(--gap-lg);
    font-size: var(--font-lg);
  }

  button.disabled {
    background-color: var(--gray);
    color: var(--lighter-gray);
  }
</style>

<button
  {type}
  class:disabled
  class:focused
  style="--color: var({color}); --text-color: var({textColor})"
  class={size}
  {disabled}
  on:click={click}
  on:focus={() => (focused = true)}
  on:blur={() => (focused = false)}>
  <slot />
  <slot name="icon" />
</button>
