const kv = await Deno.openKv("./discord_uids.sqlite");

export { kv };

export async function addDiscordUid(uid: string, matrix: string) {
  await kv.set(["discord", uid], { matrix });
}

export async function getMatrixId(uid: string): Promise<string> {
  const result = await kv.get<{matrix: string}>(["discord", uid]);
  return result.value?.["matrix"] ?? "";
}
