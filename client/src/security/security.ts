import { KeyObject, createCipheriv, createDecipheriv, createHash, createSecretKey, pbkdf2Sync, randomBytes } from "crypto";

export function secret_string(login: string, password: string, salt: string): string{
    const hash = createHash("sha256");
    hash.update(login, "utf-8");
    hash.update(password, "utf-8");
    hash.update(salt, "utf-8");
    return hash.digest("hex");
}

export function generateRandomSalt(length: number): string {
    return randomBytes(length).toString('hex');
  }

export function get_device_hash(): string{
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const cpuCores = navigator.hardwareConcurrency || 1;
    let hash = createHash('sha256')
    hash.update(timeZone);
    hash.update(cpuCores.toString());

    return hash.digest("hex");
}

/*
// Example usage:
const password = 'supersecretpassword';
const salt = crypto.randomBytes(16);

const plaintext = 'Hello, world!';
const ciphertext = CryptoHelper.encrypt(plaintext, password, salt);
console.log('Encrypted:', ciphertext);

const decryptedText = CryptoHelper.decrypt(ciphertext, password, salt);
console.log('Decrypted:', decryptedText);
*/
export class CryptoHelper {
    private static readonly algorithm = 'aes-256-gcm';
    private static readonly keyLength = 32; // 256 bits
    private static readonly ivLength = 16; // 128 bits
    private static readonly iterations = 10000;
    private static readonly digest = 'sha256';

    private static generateKeyAndIV(password: string, salt: Buffer): { key: Buffer; iv: Buffer } {
        const key = pbkdf2Sync(password, salt, CryptoHelper.iterations, CryptoHelper.keyLength, CryptoHelper.digest);

        const iv = randomBytes(CryptoHelper.ivLength);

        return { key, iv };
    }

    public static encrypt(text: string, password: string, salt: Buffer): string {
        const { key, iv } = CryptoHelper.generateKeyAndIV(password, salt);

        const cipher = createCipheriv(CryptoHelper.algorithm, key, iv);

        const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
        const tag = cipher.getAuthTag();

        return `${iv.toString('hex')}${encrypted.toString('hex')}${tag.toString('hex')}`;
    }

    public static decrypt(ciphertext: string, password: string, salt: Buffer): string | null {
        const ivHex: string = ciphertext.substring(0, CryptoHelper.ivLength * 2);
        const encryptedHex: string = ciphertext.substring(CryptoHelper.ivLength * 2, ciphertext.length - 16 * 2);
        const tagHex: string = ciphertext.substring(ciphertext.length - 16 * 2);

        const iv = Buffer.from(ivHex, 'hex');
        const encrypted = Buffer.from(encryptedHex, 'hex');
        const tag = Buffer.from(tagHex, 'hex');

        const { key } = CryptoHelper.generateKeyAndIV(password, salt);

        const decipher = createDecipheriv(CryptoHelper.algorithm, key, iv);
        decipher.setAuthTag(tag);

        try {
            const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
            return decrypted.toString('utf8');
        } catch (error: any) {
            console.error('Decryption failed:', error.message);
            return null;
        }
    }
}