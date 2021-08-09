<script lang="ts">
  import { onMount} from "svelte";
  import { InputType } from "../types/components"

  export let name : string;
  export let placeholder : string = "";
  export let type : InputType = InputType.text;
  export let value : string | number = "";
  export let label : string  = "";
  export let required : boolean = false;
  export let help : string | null = null;
  export let error : string | null = null;
  export let autofocus : boolean = false;
  
  let inputElement;
  let focused : boolean = false;

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
<div
  class="input"
  class:focused
  class:error={!!error}>
  <div class="top">
    {#if label}<label for={name}>
      {label}{#if required}<span> *</span>{/if}
    </label>{/if}
    {#if help && !error}
      <div class="help">{help}</div>
    {/if}
    {#if error}
      <div class="error">{error}</div>
    {/if}
  </div>
  <input
    bind:this={inputElement}
    {type}
    {value}
    {placeholder}
    {name}
    {required}
    on:focus={() => focused = true}
    on:blur={() => focused = false}
    on:input={handleInput} />
</div>
<style>
  .input {
    height: 5.5rem;
    padding-bottom: var(--gap-md);
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

  .focused .top .help {
    color: var(--gray);
  }

  .top .error {
    color: var(--error);
  }

  input {
    background-color: var(--gray);
    width: 100%;
    color: var(--white);
    font-size: var(--font-md);
    border: 1px double var(--transparent);
    border-radius: var(--radius);
    transition: var(--transition);
  }

  input:focus {
    border: 1px solid var(--primary);
    transition: var(--transition);
  }
</style>
