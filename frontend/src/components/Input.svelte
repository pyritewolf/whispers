<script lang="ts">
  import { onMount } from "svelte";
  import { Gap, InputType } from "../types/components";
  import type { IconName } from "../types/components";
  import Icon from "./Icon.svelte";

  export let name: string;
  export let placeholder: string = "";
  export let type: InputType = InputType.text;
  export let value: string | number = "";
  export let label: string = "";
  export let required: boolean = false;
  export let help: string | null = null;
  export let error: string | null = null;
  export let autofocus: boolean = false;
  export let readonly: boolean = false;
  export let click: Function | null = null;
  export let iconLeft: IconName | null = null;
  export let iconRight: IconName | null = null;

  let inputElement;
  let focused: boolean = false;

  const handleInput = (e) => {
    // in here, you can switch on type and implement
    // whatever behaviour you need
    value = type.match(/^(number|range)$/)
      ? parseFloat(e.target.value)
      : e.target.value;
  };

  const setFocus = () => inputElement.focus();

  onMount(() => {
    if (autofocus) setFocus();
  });
</script>

<style>
  .root {
    height: 5.5rem;
    padding-bottom: var(--gap-lg);
  }

  .top {
    display: flex;
    font-size: var(--font-sm);
    height: var(--font-md);
    justify-content: space-between;
    align-items: bottom;
    padding-bottom: var(--gap-sm);
  }

  .top label {
    flex-shrink: 0;
    font-weight: bold;
    font-size: var(--font-md);
  }

  label span {
    color: var(--error);
  }

  .top .help {
    color: transparent;
    transition: var(--transition);
  }

  .focused .top .help,
  .clickable .top .help {
    color: var(--lighter-gray);
  }

  .top .error {
    color: var(--error);
  }

  .input {
    background-color: var(--gray);
    color: var(--white);
    font-size: var(--font-md);
    border: 1px solid var(--transparent);
    border-radius: var(--radius);
    transition: var(--transition);
    display: flex;
    align-items: center;
    padding: var(--gap-sm);
    gap: var(--gap-sm);
  }

  input {
    background-color: var(--transparent);
    color: var(--white);
    width: 100%;
    font-size: inherit;
    border: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0;
  }

  .input:focus {
    border: 1px solid var(--primary);
    transition: var(--transition);
  }

  .clickable,
  .clickable input {
    cursor: pointer;
  }
</style>

<div
  class="root"
  class:focused
  class:error={!!error}
  class:clickable={click !== null}
  on:click={() => click !== null && click()}>
  <div class="top">
    {#if label}
      <label for={name}>
        {label}{#if required}<span> *</span>{/if}
      </label>
    {/if}
    {#if help && !error}
      <div class="help">{help}</div>
    {/if}
    {#if error}
      <div class="error">{error}</div>
    {/if}
  </div>
  <div class="input">
    {#if iconLeft}
      <Icon name={iconLeft} />
    {/if}
    <input
      bind:this={inputElement}
      {type}
      {value}
      {placeholder}
      {name}
      {required}
      {readonly}
      on:focus={() => (focused = true)}
      on:blur={() => (focused = false)}
      on:input={handleInput} />
    {#if iconRight !== null}
      <Icon name={iconRight} />
    {/if}
  </div>
</div>
