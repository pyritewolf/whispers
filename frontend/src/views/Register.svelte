<script lang="ts">
  import { Link } from "svelte-navigator";
  import { paths } from "../constants";
  import AuthLayout from "../layouts/AuthLayout.svelte";
  import Input from "../components/Input.svelte";
  import Button from "../components/Button.svelte";
  import { Color, InputType } from "../types/components";

  const formData = {
    email: "",
    password: "",
    confirmPassword: "",
    username: "",
  };

  const handleSubmit = () => {
    fetch("/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });
  };
</script>

<style>
  h1 {
    text-align: center;
    padding-bottom: var(--gap-md);
  }

  p {
    text-align: center;
  }
</style>

<AuthLayout>
  <h1>Sign up</h1>
  <form on:submit|preventDefault={handleSubmit}>
    <p>
      Already got an account?
      <Link to={paths.LOGIN}>Log in</Link>!
    </p>
    <Input
      autofocus={true}
      label="E-mail"
      placeholder="coolstreamer@gmail.com"
      bind:value={formData.email}
      name="email" />
    <Input
      label="Username"
      placeholder="coolstreamer69"
      bind:value={formData.username}
      name="username" />
    <Input
      label="Password"
      type={InputType.password}
      placeholder="safetaters69"
      bind:value={formData.password}
      name="password" />
    <Input
      label="Repeat password"
      type={InputType.password}
      placeholder="safetaters69"
      bind:value={formData.confirmPassword}
      name="confirm-password" />
    <Button color={Color.primary}>Get started</Button>
  </form>
</AuthLayout>
