// https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/api/client/register/register.rs#L22
export const RANDOM_USER_ID_LENGTH = 10;
// https://github.com/matrix-construct/tuwunel/blob/5ff48622a03f6dcf110a59c8369611375b649037/src/admin/user/mod.rs#L35
export const AUTO_GEN_PASSWORD_LENGTH = 25;

export function randomAlphaNumeric(length: number): string {
  let s = '';
  while (s.length < length) {
    s += Math.random().toString(36).slice(2);
  }
  return s.substring(0, length);
}
