export async function hashPassword(password: string): Promise<string> {
  const buffer = new TextEncoder().encode(password)
  const digest = await crypto.subtle.digest('SHA-256', buffer)
  return Array.from(new Uint8Array(digest))
    .map((byte) => byte.toString(16).padStart(2, '0'))
    .join('')
}
