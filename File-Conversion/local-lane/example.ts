// Reference only: this is the local lane, so it runs in the user's browser via
// WebAssembly, not in this project's Python code. Ship it in your web app.
//
//   npm install @hushvert/engine

import { convertFile } from '@hushvert/engine'

// Images (HEIC, PNG, JPG, WebP, AVIF, JXL) need no configuration.
export async function heicToJpg(heicFile: File): Promise<Blob> {
  return convertFile(
    heicFile,
    { from: 'heic', to: 'jpg', module: 'images' },
    (pct) => console.log(`${pct}%`),
  )
  // The returned Blob never left the browser - no network request is made.
}

// Heavier codecs (audio, video, archives, PDF page ops) run from WASM workers
// your app serves, wired up once via a `configureEngine(...)` call pointing
// at those assets.
