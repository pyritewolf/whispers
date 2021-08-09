<script lang="ts">
  import { Link } from "svelte-navigator";
  import {paths} from "../constants"
  import AuthLayout from "../layouts/AuthLayout.svelte"
  import Input from "../components/Input.svelte"
  import Button from "../components/Button.svelte";
import { Color } from "../types/components";

  const formData = {
    email: "",
    password: "",
    confirmPassword: "",
    username: "",
  };

  const handleSubmit = () => {
    console.log(formData)
  };
</script>

<AuthLayout>
  <h1>Sign up</h1>
  <form on:submit|preventDefault={handleSubmit}>
    <p>Already got an account? <Link to={paths.LOGIN}>Log in</Link>!</p>
    <Input autofocus={true} label="E-mail" placeholder="coolstreamer@gmail.com" value={formData.email} name="email"/>
    <Input label="Username" placeholder="coolstreamer69" value={formData.username} name="username"/>
    <Input label="Password" placeholder="safetaters69" value={formData.password} name="password"/>
    <Input label="Repeat password" placeholder="safetaters69" value={formData.confirmPassword} name="confirm-password"/>
    <Button color={Color.primary}>Get started</Button>
  </form>
</AuthLayout>

<style>
  h1 {
    text-align: center;
    padding-bottom: var(--gap-md);
  }

  p {
    text-align: center;
  }
</style>
