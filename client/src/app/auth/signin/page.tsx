'use client'

import { device } from "@/api/api";
import { APISignIn } from "@/api/authentication/signin";
import NavBar from "@/components/NavBar";
import { CryptoHelper, generateRandomSalt, get_device_hash } from "@/security/security";
import { Validation } from "@/utils/validation";
import { Typography, TextField, Button, Alert, Box, MenuItem, Select, FormControl, InputLabel, Grid, Link } from "@mui/material";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

export default function(){
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [privateKey, setPrivateKey] = useState('');
    const [expiration, setExpiration] = useState('');
    const [oneTimeCode, setOneTimeCode] = useState('');
    const [oneTimeCodeType, setOneTimeCodeType] = useState('basic');
    const [response, setResponse] = useState(null);

    const handleSignIn = async () => {
      let validation = new Validation();
      if (
        !login ||
        !password ||
        !(await validation.is_password(password)) ||
        !validation.is_number(expiration) ||
        !validation.is_number(oneTimeCode)
      ) {
        alert(
          'Fields are filled in incorrectly. Please fill in both login and password fields. Password must contain at least 1 lowercase character, 1 uppercase character, 1 number, 1 special character'
        );
        return;
      }
  
      try {
        let apiSignIn = new APISignIn(login, password, privateKey, oneTimeCode, expiration, device);
        const apiResponse = await apiSignIn.execute(oneTimeCodeType);
        setResponse(apiResponse);
      } catch (error: any) {
        console.error('API error:', error);
        setResponse(error);
      }
    };
    
    useEffect(() => {
      const processSignIn = () => {
        if (response && response.status === 200) {
          let local_key: string = generateRandomSalt(16);
          let encrypt_password = CryptoHelper.encrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));
          let encrypt_private_key = CryptoHelper.encrypt(privateKey, get_device_hash(), Buffer.from(local_key, 'utf-8'));
  
          // Store in session storage instead of local storage
          localStorage.setItem('secure', JSON.stringify({
            'password': encrypt_password,
            'private_key': encrypt_private_key,
            'token': response.data.token,
            'local_key': local_key
          }));
  
          redirect('/');
        }
      };
  
      processSignIn();
    }, [response, password, privateKey]);

    return (
      <Box maxWidth={600} m="auto" p={3}>
        <div>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Login"
                autoFocus
                onChange={(e) => setLogin(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Password"
                type="password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Private Key"
                type="password"
                onChange={(e) => setPrivateKey(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Token expiration time (minutes)"
                onChange={(e) => setExpiration(e.target.value)}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="One Time Code"
                onChange={(e) => setOneTimeCode(e.target.value)}
              />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth margin="none">
                <InputLabel htmlFor="one-time-code-type">One Time Code Type</InputLabel>
                <Select
                  label="One Time Code Type"
                  value={oneTimeCodeType}
                  onChange={(e) => setOneTimeCodeType(e.target.value)}
                >
                  <MenuItem value="basic">Basic</MenuItem>
                  <MenuItem value="backup">Backup</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <Button fullWidth variant="contained" color="primary" onClick={handleSignIn}>
                Sign In
              </Button>
            </Grid>
            <Grid item xs={12}>
                <Link href="/auth/signup">
                    <a>Don&apos;t have an account? Register here</a>
                </Link>
            </Grid>
          </Grid>
          {response && (
          <Alert severity={response.status === 200 ? 'success' : 'error'}>
            {response.status === 200 ? 'Sign in successful' : response.data.msg.en}
          </Alert>
        )}
        </div>
      </Box>
    );
  }