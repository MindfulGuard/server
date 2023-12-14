'use client'

import {APISignUp} from "@/api/authentication/signup";
import { Validation } from "@/utils/validation";
import { Box, Typography, Alert, TextField, Button, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Table, Link } from "@mui/material";
import { QRCodeCanvas } from "qrcode.react";
import { useState } from "react";

export default function SignUpForm() {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [private_key, setPrivateKey] = useState('');
  const [response, setResponse] = useState();
  const [displayTotp, setDisplayTotp] = useState(false);

  const handleSignUp = async () => {
    let validation = new Validation();
    if (!login || !password || !(await validation.is_password(password))) {
      alert(
        'Please fill in both login and password fields. Password must contain at least 1 lowercase character, 1 uppercase character, 1 number, 1 special character'
      );
      return;
    }

    try {
      let uuid = crypto.randomUUID();
      let api_signup = new APISignUp(login, password, uuid);
      const apiResponse = await api_signup.execute();
      setPrivateKey(uuid);
      setResponse(apiResponse);
    } catch (error: any) {
      console.error('API error:', error);
      setResponse(error);
    }
  };

  const handleToggleTotpDisplay = () => {
    setDisplayTotp(!displayTotp);
  };

  return (
    <Box maxWidth={600} m="auto" p={3}>
      <TextField
        label="Login"
        fullWidth
        value={login}
        onChange={(e) => setLogin(e.target.value)}
        variant="outlined"
        margin="normal"
        placeholder="Enter your login"
      />
      <TextField
        label="Password"
        fullWidth
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        type="password"
        variant="outlined"
        margin="normal"
        placeholder="Enter your password"
      />
      <Button variant="contained" color="primary" onClick={handleSignUp}>
        Sign Up
      </Button>
      
      <Box mt={3}>
        <Link href="/auth/signin">
          <a>Already have an account? Sign in here</a>
        </Link>
      </Box>

      {response && response.data && response.status === 200 && (
        <Box mt={3}>
          <Typography variant="h6">Private key: <span style={{ color: 'red' }}>{private_key}</span></Typography>
          <p></p>
          <Button variant="outlined" color="primary" onClick={handleToggleTotpDisplay}>
            Toggle Totp code
          </Button>
          
          {/* Display Totp code based on state */}
          {displayTotp && (
            <Typography variant="h6">
              Totp code: <span style={{ color: 'red' }}>{response.data.secret_code}</span>
            </Typography>
          )}
          <Typography variant="h6">QR Code:</Typography>
          <QRCodeCanvas value={`otpauth://totp/${login}?secret=${response.data.secret_code}&issuer=MindfulGuard`} size={256} />
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Backup Codes</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {response.data.backup_codes.map((item: any, index: number) => (
                  <TableRow key={index}>
                    <TableCell>{item}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}
      <p></p>
      {response && response.data && response.status !== 200 && (
        <Alert severity="error">{response.data.msg.en}</Alert>
      )}
    </Box>
  );
}