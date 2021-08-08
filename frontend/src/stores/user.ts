import { writable } from 'svelte/store';
import type { User } from '../types/entities';

export default writable<User | null>(null);
