import { R2 } from "@cloudflare/r2-client";

const r2 = new R2({
  accountId: process.env.CLOUDFLARE_ACCOUNT_ID!,
  accessKeyId: process.env.ACCESS_KEY_ID!,
  secretAccessKey: process.env.SECRET_ACCESS_KEY!,
});

export async function getImageUrl(key: string): Promise<string> {
  return r2.getSignedUrl({
    bucket: process.env.BUCKET_NAME!,
    key,
    expiresIn: 3600,
  });
}

// Fetch as buffer (for processing)
export async function getImageBuffer(key: string): Promise<Buffer> {
  const command = new GetObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: key,
  });
  const response = await s3.send(command);
  // Convert stream to buffer
  const stream = response.Body as any;
  const chunks: Uint8Array[] = [];
  for await (const chunk of stream) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}
