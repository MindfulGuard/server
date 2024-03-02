'use client'

import { APISignOut } from "@/api/authentication/signout";
import { APIUserGet } from "@/api/user/get";
import { AppBar, Toolbar, Typography, CircularProgress, Button, Popover, Link, Modal, TextField, Select, MenuItem, Box, Alert, Paper, TableHead, TableCell, TableRow, TableBody, Table, TableContainer } from "@mui/material";
import { redirect } from "next/navigation";
import MicrosoftIcon from '@mui/icons-material/Microsoft';
import WebIcon from '@mui/icons-material/Web';
import AndroidIcon from '@mui/icons-material/Android';
import AppleIcon from '@mui/icons-material/Apple';
import TerminalIcon from '@mui/icons-material/Terminal';
import DevicesIcon from '@mui/icons-material/Devices';
import { SyntheticEvent, useEffect, useState } from "react";
import { APIUserUpdateSecretOrBackupCode } from "@/api/user/update_secret_or_backup_code";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { QRCodeCanvas } from "qrcode.react";
import { Validation } from "@/utils/validation";
import { APIUserUpdateSecretString } from "@/api/user/update_secret_string";
import { APIUserDeleteAccount } from "@/api/user/delete_account";


function NavBar() {
    const [token, setToken] = useState('');
    const [anchorEl, setAnchorEl] = useState(null);
    const [response, setResponse] = useState(null);
    const [openModal, setOpenModal] = useState(false);
    const [openModalSettings, setOpenModalSettings] = useState(false);
    const [openModalInformation, setOpenModalInformation] = useState(false);
    const [selectedToken, setSelectedToken] = useState(null);
    const [secretString, setSecretString] = useState('')
    const [secretStringNew, setSecretStringNew] = useState('')
    const [privateString, setPrivateString] = useState('')
    const [oneTimeCode, setOneTimeCode] = useState('')
    const [oneTimeCodeType, setOneTimeCodeType] = useState('basic')
    const [valueTab, setValueTab] = useState('1');
    const [resultSettings, setResultSettings] = useState(null)
    
    const handleChangeTab = (event: SyntheticEvent, newValue: string) => {
      setValueTab(newValue);
    };

    const handleClick = (event: any, token: any) => {
      setAnchorEl(event.currentTarget);
      setSelectedToken(token);
    };

    const handleClose = () => {
      setAnchorEl(null);
      setSelectedToken(null);
    };

    const handleOpenModal = () => {
      setOpenModal(true);
      handleClose();
    };

    const handleOpenModalSettings = () => {
      setOpenModalSettings(true);
      handleCloseModal();
    }

    const handleOpenModalInfo = () => {
      setOpenModalInformation(true);
      handleCloseModal();
    }
    
    const handleUpdateSecretString = async () =>{
      try{
        let validation = new Validation();
        if (!await validation.is_password(secretStringNew)){
          setResultSettings(
            <Alert severity="error">Password must contain at least 1 lowercase character, 1 uppercase character, 1 number, 1 special character</Alert>
          )
          return
        }
        const login: any = response&&response.data.information.username
        let api = new APIUserUpdateSecretString(
          token,
          login,
          secretString,
          privateString,
          secretStringNew,
          oneTimeCode
        )
        let reult = await api.execute()
        setResultSettings(
          <Alert severity="success">{reult&&reult.data.msg.en}</Alert>
        )
      }catch(error){
        setResultSettings(
          <Alert severity="error">{error.data.msg.en}</Alert>
        )
      }
    }

    const handleDeleteAccount = async () =>{
      try{
        const login: any = response&&response.data.information.username
        let api = new APIUserDeleteAccount(token, login, secretString, privateString, oneTimeCode)
        await api.execute()
        location.reload()
      }catch(error){
        setResultSettings(
          <Alert severity="error">{error.data.msg.en}</Alert>
        )
      }
    }

    const handleUpdateSecretOrBackupCode = async () => {
      try{
        const login: any = response&&response.data.information.username
        let api = new APIUserUpdateSecretOrBackupCode(token, login, secretString, privateString)
        let resp = await api.execute(oneTimeCodeType)

        if (typeof (resp&&resp.data.data) == "string"){
          setResultSettings(
            <>
            <Alert severity="success">{resp&&resp.data.msg.en}</Alert>
            <Typography variant="h6">
                Totp code: <span style={{ color: 'red' }}>{resp.data.data}</span>
              </Typography>
            <Typography variant="h6">QR Code:</Typography>
            <QRCodeCanvas value={`otpauth://totp/${login}?secret=${resp.data.data}&issuer=MindfulGuard`} size={128} />
            </>
          )
        }else{
          setResultSettings(
            <>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Backup Codes</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {resp.data.data.map((item: any, index: number) => (
                    <TableRow key={index}>
                      <TableCell>{item}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            </>
          )
        }
      }catch(error){
        console.log(error)
        setResultSettings(<Alert severity="error">Failed</Alert>)
        return
      }
    }

    const handleCloseModalInfo = () => {
      setOpenModalInformation(false);
    };

    const handleCloseModalSettings = () => {
      setOpenModalSettings(false);
      setSecretString('')
      setSecretStringNew('')
      setPrivateString('')
      setOneTimeCode('')
      setValueTab('1')
      setResultSettings(null)
    };

    const handleCloseModal = () => {
      setOpenModal(false);
    };

    const defineDeviceIcon = (deviceName: string)=>{
      let lowercaseString = deviceName.toLowerCase();

      if (lowercaseString.includes("web")) {
          return <WebIcon/>
      } else if (lowercaseString.includes("windows")) {
          return <MicrosoftIcon/>;
      } else if (lowercaseString.includes("linux")) {
          return <TerminalIcon/>
      } else if (lowercaseString.includes("android")) {
          return <AndroidIcon/>
      } else if (lowercaseString.includes("ios")) {
          return <AppleIcon/>
      } else {
          return <DevicesIcon/>
      }
    }

    const handleLogout = async (tokenId: string) => {
      try {
        let api = new APISignOut(token, tokenId);
        let response = await api.execute();
        console.log("Hello");
        if (response.status === 200) {
          console.log(response.status);
          // Update the state with the filtered tokens
          setResponse((prevResponse) => ({
            ...prevResponse,
            data: {
              ...prevResponse.data,
              tokens: prevResponse.data.tokens.filter((t: any) => t.id !== tokenId),
            },
          }));
        }
      } catch (error: any) {
        return;
      }
    };

    const fetchData = async () => {
        try {
            const secureDataString = localStorage.getItem('secure');
            if (secureDataString !== null) {
                let secureData = JSON.parse(secureDataString);
                const currentToken = secureData ? secureData.token : '400';
                setToken(currentToken);
                let apiSignIn = new APIUserGet(currentToken);
                const apiResponse = await apiSignIn.execute();
                setResponse(apiResponse);
            } else {
                console.error('secureDataString is null');
                return;
            }
        } catch (error: any) {
            console.error('API error:', error);
            setResponse(error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        if (response && response.status !== 200) {
            redirect('/auth/signin');
        }
    }, [response]);

    if (!response) {
        return (
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6">Loading...</Typography>
                    <CircularProgress color="inherit" size={20} style={{ marginLeft: '10px' }} />
                </Toolbar>
            </AppBar>
        );
    }

    if (!response || !response.data) {
        return (
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6">Loading...</Typography>
              <CircularProgress color="inherit" size={20} style={{ marginLeft: '10px' }} />
            </Toolbar>
          </AppBar>
        );
      }
      
      const { information } = response.data;

      const open = Boolean(anchorEl);
      const id = open ? 'simple-popover' : undefined;

      return (
        <>
            <AppBar position="static">
                <Toolbar>
                    <div style={{ display: 'flex', marginRight: 'auto'}}>
                        <Link href="/">
                        <Typography variant="h6" style={{ cursor: 'pointer',  color: 'white' }}>
                            MindfulGuard
                        </Typography>
                        </Link>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', marginLeft: 'auto' }}>
                        <div>
                            <Typography variant="h6" onClick={handleClick} style={{ cursor: 'pointer' }}>
                                {information?.username}
                            </Typography>
                            <Popover id={id} open={open} anchorEl={anchorEl} onClose={handleClose} anchorOrigin={{
                            vertical: 'bottom',
                            horizontal: 'right',
                        }} transformOrigin={{
                            vertical: 'top',
                            horizontal: 'right',
                        }}>
                                <div style={{ display: 'flex', flexDirection: 'column', padding: '10px' }}>
                                    <Button onClick={handleOpenModalInfo}>Information</Button>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', padding: '10px' }}>
                                    <Button onClick={handleOpenModalSettings}>Settings</Button>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', padding: '10px' }}>
                                    <Button onClick={handleOpenModal}>Logout</Button>
                                </div>
                            </Popover>

                            <style jsx>{`
                              .scroll-container {
                                overflow-y: auto;
                                max-height: 80vh;
                                padding-right: 15px;
                              }

                              .scroll-container::-webkit-scrollbar {
                                width: 10px;
                              }

                              .scroll-container::-webkit-scrollbar-thumb {
                                background-color: #1976D2;
                                border-radius: 5px;
                              }

                              .scroll-container::-webkit-scrollbar-track {
                                background-color: #f1f1f1;
                              }
                            `}</style>
                            <Modal open={openModalInformation} onClose={handleCloseModalInfo}>
                                <div className="scroll-container" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)', maxHeight: '80vh', overflowY: 'auto' }}>
                                    <h2 style={{ marginBottom: '20px', textAlign: 'center' }}>User Information</h2>
                                      <div style={{ marginBottom: '15px', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
                                        <Typography>Username: {response.data&&response.data.information.username}</Typography>
                                        <div style={{ marginBottom: '15px', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}></div>
                                        <Typography>Registration ip: {response.data&&response.data.information.ip}</Typography>
                                        <div style={{ marginBottom: '15px', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}></div>
                                        <Typography>Created at: {new Date(response.data&&response.data.information.created_at * 1000).toLocaleString()}</Typography>
                                      </div>
                                    <Button onClick={handleCloseModalInfo} style={{ marginTop: '10px' }}>Close</Button>
                                </div>
                            </Modal> 
                            <Modal open={openModal} onClose={handleCloseModal}>
                                <div className="scroll-container" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)', maxHeight: '80vh', overflowY: 'auto' }}>
                                    <h2 style={{ marginBottom: '20px', textAlign: 'center' }}>Tokens Information</h2>
                                    {response && response.data && response.data.tokens && response.data.tokens.map((token: any) => (
                                      <div key={token.id} style={{ marginBottom: '15px', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
                                          <p style={{ fontWeight: 'bold', marginBottom: '5px' }}>Token ID: {token.id}</p>
                                          <p>Device: {token.device} {defineDeviceIcon(token.device)}</p>
                                          <p>Created at: {new Date(token.created_at * 1000).toLocaleString()}</p>
                                          <p>Updated at: {new Date(token.updated_at * 1000).toLocaleString()}</p>
                                          <p>Last IP: {token.last_ip}</p>
                                          <p>Expiration: {new Date(token.expiration * 1000).toLocaleString()}</p>
                                          <Button onClick={() => handleLogout(token.id)}>Terminate Session</Button>
                                      </div>
                                  ))}

                                    <Button onClick={handleCloseModal} style={{ marginTop: '10px' }}>Close</Button>
                                </div>
                            </Modal>

                            <Modal open={openModalSettings} onClose={handleCloseModalSettings}>
                                <div className="scroll-container" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)', maxHeight: '80vh', overflowY: 'auto' }}>
                                    <h2 style={{ marginBottom: '20px', textAlign: 'center' }}>Settings</h2>
                                    <Box sx={{ width: '100%' }}>
                                      <Tabs
                                        value={valueTab}
                                        onChange={handleChangeTab}
                                        aria-label=""
                                      >
                                        <Tab
                                          value="1"
                                          label="Update one time or backup code"
                                          wrapped
                                        />
                                        <Tab
                                          value="2"
                                          label="Update password"
                                          wrapped
                                        />
                                        <Tab
                                          value="3"
                                          label="Delete account"
                                          wrapped
                                        />
                                      </Tabs>
                                    </Box>
                                    {valueTab === "1" && (
                                      <>
                                        <TextField
                                          label="Password"
                                          fullWidth
                                          type="password"
                                          value={secretString}
                                          onChange={(e) => setSecretString(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your password"
                                        />
                                        <TextField
                                          label="Private String"
                                          fullWidth
                                          type="password"
                                          value={privateString}
                                          onChange={(e) => setPrivateString(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your private string"
                                        />
                                        <Select
                                          label="One Time Code Type"
                                          value={oneTimeCodeType}
                                          onChange={(e) => setOneTimeCodeType(e.target.value)}
                                        >
                                          <MenuItem value="basic">Basic</MenuItem>
                                          <MenuItem value="backup">Backup</MenuItem>
                                        </Select>
                                        <p></p>
                                        <Button onClick={handleUpdateSecretOrBackupCode}>Send</Button>
                                      </>
                                    )}
                                    {valueTab === "2" && (
                                      <>
                                        <TextField
                                          label="Old Password"
                                          fullWidth
                                          type="password"
                                          value={secretString}
                                          onChange={(e) => setSecretString(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your old password"
                                        />
                                        <TextField
                                          label="Private String"
                                          fullWidth
                                          type="password"
                                          value={privateString}
                                          onChange={(e) => setPrivateString(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your private string"
                                        />
                                        <TextField
                                          label="New password"
                                          fullWidth
                                          type="password"
                                          value={secretStringNew}
                                          onChange={(e) => setSecretStringNew(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your new password"
                                        />
                                        <TextField
                                          label="One Time Code"
                                          fullWidth
                                          type="number"
                                          value={oneTimeCode}
                                          onChange={(e) => setOneTimeCode(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your one time code"
                                        />
                                        
                                        <Button onClick={handleUpdateSecretString}>Send</Button>
                                      </>
                                    )}
                                    {valueTab === "3" && (
                                      <>
                                        <TextField
                                          label="Password"
                                          fullWidth
                                          type="password"
                                          value={secretString}
                                          onChange={(e) => setSecretString(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your password"
                                        />
                                        <TextField
                                          label="Private String"
                                          fullWidth
                                          type="password"
                                          value={privateString}
                                          onChange={(e) => setPrivateString(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your private string"
                                        />
                                        <TextField
                                          label="One Time Code"
                                          fullWidth
                                          type="number"
                                          value={oneTimeCode}
                                          onChange={(e) => setOneTimeCode(e.target.value)}
                                          variant="outlined"
                                          margin="normal"
                                          placeholder="Enter your one time code"
                                        />
                                        <Button color="error" onClick={handleDeleteAccount}>Delete</Button>
                                      </>
                                    )}
                                    <span>
                                      {resultSettings}
                                    </span>
                                    <p></p>
                                    <Button onClick={handleCloseModalSettings} style={{ marginTop: '10px' }}>Close</Button>
                                </div>
                            </Modal>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                            {/* Here you can add any additional content on the right side */}
                        </div>
                    </div>
                </Toolbar>
            </AppBar>
        </>
    );
}

export default NavBar