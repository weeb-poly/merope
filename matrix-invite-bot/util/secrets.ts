import process from "node:process";
import fs from 'node:fs/promises';
import { pathToFileURL } from "node:url";

import { assert } from "@std/assert";

export async function getMatrixCreds(): Promise<{
  user: string;
  homeserver: string;
  password: string;
}> {
  const CREDENTIALS_DIRECTORY = process.env["CREDENTIALS_DIRECTORY"] || process.cwd();
  const credDirUrl = CREDENTIALS_DIRECTORY ? pathToFileURL(CREDENTIALS_DIRECTORY) : null;

  const userId = process.env["MATRIX_USER"];
  assert(userId);

  const [ user, _homeserver ] = userId.split(":", 2);

  const homeserver = process.env["MATRIX_SERVER"] || `https://${_homeserver}`;
  assert(homeserver);

  let password = process.env["MATRIX_PASSWORD"];
  if (!password) {
    assert(credDirUrl);
    password = await fs.readFile(new URL("/password", credDirUrl), { encoding: 'utf8' });
  }

  assert(password);

  return { user, homeserver, password };
}
