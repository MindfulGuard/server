'use client'

import { useCallback, useEffect, useState } from 'react';
import { APIGetAllItems } from '@/api/items/get';
import NavBar from '@/components/NavBar';
import {
  Typography,
  Paper,
  Container,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress,
  LinearProgress,
  Box,
  createTheme,
  ThemeProvider,
  Button,
  IconButton,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Tooltip,
  Input,
  MenuItem,
  Select,
  Menu,
} from '@mui/material';
import StarIcon from '@mui/icons-material/Star';
import StarBorderPurple500SharpIcon from '@mui/icons-material/StarBorderPurple500Sharp';
import { APIFileDownload } from '@/api/files/download';
import AddIcon from '@mui/icons-material/Add';
import { redirect, useRouter } from 'next/navigation';
import { APISafeCreate } from '@/api/items/safe/create';
import { CryptoHelper, get_device_hash } from '@/security/security';
import DeleteIcon from '@mui/icons-material/Delete';
import { APISafeDelete } from '@/api/items/safe/delete';
import EditIcon from '@mui/icons-material/Edit';
import { APISafeUpdate } from '@/api/items/safe/update';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { APIFileUpload } from '@/api/files/upload';
import { APIFileDelete } from '@/api/files/delete';
import { APIFavorite } from '@/api/items/favorite';
import { APICreateItem } from '@/api/items/create';
import { APISettings } from '@/api/settings';
import DeleteOutlineOutlinedIcon from '@mui/icons-material/DeleteOutlineOutlined';
import { APIDeleteItem } from '@/api/items/delete';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { APIMoveItem } from '@/api/items/move';

const ScrollableContainer = ({ children, maxHeight }) => (
  <div style={{
    maxHeight,
    overflowY: 'auto',
    paddingRight: '15px',
  }}>
    {children}
    <style jsx>{`
      div {
        scrollbar-width: thin;
        scrollbar-color: #1976D2 #f1f1f1;
      }

      ::-webkit-scrollbar {
        width: 10px;
      }

      ::-webkit-scrollbar-thumb {
        background-color: #1976D2;
        border-radius: 5px;
      }

      ::-webkit-scrollbar-track {
        background-color: #f1f1f1;
      }
    `}</style>
  </div>
);

const EditModal = ({ open, onClose, onSave, name, description, loading, setName, setDescription, private_key, password, local_key }) => {
  const [decryptedDescription, setDecryptedDescription] = useState('');

  useEffect(() => {
    const decryptData = async () => {
      try {
        const decryptPrivateKey = await CryptoHelper.decrypt(private_key, get_device_hash(), Buffer.from(local_key, 'utf-8'));
        const decryptPassword = await CryptoHelper.decrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));
        const decryptedDesc = await CryptoHelper.decrypt(description, decryptPassword, decryptPrivateKey);
        setDecryptedDescription(decryptedDesc);
      } catch (error) {
        console.error('Error decrypting data:', error);
      }
    };

    decryptData();
  }, [description, password, private_key, local_key]);

  const handleSave = async () => {
    try {
      const decryptPrivateKey = await CryptoHelper.decrypt(private_key, get_device_hash(), Buffer.from(local_key, 'utf-8'));
      const decryptPassword = await CryptoHelper.decrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));
      const encryptDescription = await CryptoHelper.encrypt(decryptedDescription, decryptPassword, decryptPrivateKey);
      onSave(name, encryptDescription); // Pass the encrypted description to onSave callback
    } catch (error) {
      console.error('Error encrypting data:', error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Edit Safe</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Name"
          type="text"
          fullWidth
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          margin="dense"
          label="Description"
          type="text"
          fullWidth
          value={decryptedDescription}
          onChange={(e) => setDecryptedDescription(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary" disabled={loading}>
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary" disabled={loading}>
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const SafeList = ({ safes, onSelectSafe, onDeleteSafe, handleEditClick }) => (
  <ScrollableContainer maxHeight="500px">
    <List style={{ marginLeft: 0 }}>
      {safes.map((safe) => (
        <ListItem button key={safe.id} onClick={() => onSelectSafe(safe)}>
          <ListItemText primary={safe.name} secondary={`Items: ${safe.count_items}`} />
          <IconButton onClick={() => handleEditClick(safe)}><EditIcon/></IconButton>
          <IconButton onClick={() => onDeleteSafe(safe.id)}><DeleteIcon/></IconButton>
        </ListItem>
      ))}
    </List>
  </ScrollableContainer>
);

const theme = (color: string)=> {
  return createTheme({
  palette: {
    primary: {
      main: color,
    },
  },
})};

const EditModalItem = ({ open, onClose, onSave, data, token, safe_id, catigories, types, dataState, local_key, password, private_key }) => {
  const [editedData, setEditedData] = useState({
    title: data.title || '',
    category: data.category || '',
    notes: data.notes || '',
    tags: data.tags ? [...data.tags] : [],
    sections: data.sections ? [...data.sections] : [],
  });

  const handleInputChange = (field, value) => {
    setEditedData((prevData) => ({
      ...prevData,
      [field]: value,
    }));
  };

  const handleTagChange = (tagIndex, value) => {
    setEditedData((prevData) => {
      const updatedTags = [...prevData.tags];
      updatedTags[tagIndex] = value;
      return {
        ...prevData,
        tags: updatedTags,
      };
    });
  };

  const handleAddTag = () => {
    setEditedData((prevData) => ({
      ...prevData,
      tags: [
        ...(prevData.tags || []),
        '',
      ],
    }));
  };

  const handleFieldChange = (sectionIndex, fieldIndex, field, value) => {
    setEditedData((prevData) => {
      const sections = [...prevData.sections];
      const fields = [...sections[sectionIndex].fields];
      fields[fieldIndex] = {
        ...fields[fieldIndex],
        [field]: value,
      };
      sections[sectionIndex] = {
        ...sections[sectionIndex],
        fields,
      };
      return {
        ...prevData,
        sections,
      };
    });
  };

  const handleAddSection = () => {
    setEditedData((prevData) => {
      const sections = prevData.sections || [];
      const initSectionExists = sections.some((section) => section.section === 'INIT');
  
      if (!initSectionExists) {
        // If "INIT" section doesn't exist, add it
        return {
          ...prevData,
          sections: [
            ...sections,
            {
              section: 'INIT',
              fields: [],
            },
          ],
        };
      }
  
      return {
        ...prevData,
        sections: [
          ...sections,
          {
            section: 'New Section',
            fields: [],
          },
        ],
      };
    });
  };

  const handleSectionNameChange = (sectionIndex, value) => {
    setEditedData((prevData) => {
      const sections = [...prevData.sections];
      sections[sectionIndex] = {
        ...sections[sectionIndex],
        section: value,
      };
      return {
        ...prevData,
        sections,
      };
    });
  };

  const handleAddField = (sectionIndex) => {
    setEditedData((prevData) => {
      const sections = [...prevData.sections];
      sections[sectionIndex] = {
        ...sections[sectionIndex],
        fields: [
          ...sections[sectionIndex].fields,
          {
            type: 'STRING',
            label: '', // Default empty label
            value: '',
          },
        ],
      };
      return {
        ...prevData,
        sections,
      };
    });
  };

  const handleDeleteSection = (sectionIndex) => {
    setEditedData((prevData) => {
      const updatedSections = [...prevData.sections];
      updatedSections.splice(sectionIndex, 1);
      return {
        ...prevData,
        sections: updatedSections,
      };
    });
  };

  const handleDeleteField = (sectionIndex, fieldIndex) => {
    setEditedData((prevData) => {
      const sections = [...prevData.sections];
      const updatedFields = [...sections[sectionIndex].fields];
      updatedFields.splice(fieldIndex, 1);
      sections[sectionIndex] = {
        ...sections[sectionIndex],
        fields: updatedFields,
      };
      return {
        ...prevData,
        sections,
      };
    });
  };

  const handleDeleteTag = (tagIndex) => {
    setEditedData((prevData) => {
      const updatedTags = [...prevData.tags];
      updatedTags.splice(tagIndex, 1);
      return {
        ...prevData,
        tags: updatedTags,
      };
    });
  };


  const handleSaveClick = async () => {
    try {
      const decryptPrivateKey = CryptoHelper.decrypt(private_key, get_device_hash(), Buffer.from(local_key, 'utf-8'));
      const decryptPassword = CryptoHelper.decrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));
      // Encrypt notes field
      const encryptedNotes = CryptoHelper.encrypt(editedData.notes, decryptPassword, decryptPrivateKey);
  
      // Encrypt value fields in parallel
      const encryptedSections = await Promise.all(
        editedData.sections.map(async (section) => {
          const encryptedFields = await Promise.all(
            section.fields.map(async (field) => ({
              ...field,
              value: await CryptoHelper.encrypt(field.value, decryptPassword, decryptPrivateKey),
            }))
          );
          return {
            ...section,
            fields: encryptedFields,
          };
        })
      );
  
      const encryptedData = {
        ...editedData,
        notes: encryptedNotes,
        sections: encryptedSections,
      };
  
      let api = new APICreateItem(token);
      await api.execute(safe_id, encryptedData);
      onClose();
      const updatedData = await new APIGetAllItems(token).execute();
      dataState(updatedData.data);
    } catch (error) {
      console.error('Error saving item:', error);
      // Handle the error as needed, e.g., display an error message to the user
    }
  };

  const handleCategoryChange = (value) => {
    setEditedData((prevData) => ({
      ...prevData,
      category: value,
    }));
  };

  const handleTypeChange = (sectionIndex, fieldIndex, value) => {
    setEditedData((prevData) => {
      const sections = [...prevData.sections];
      const fields = [...sections[sectionIndex].fields];
      fields[fieldIndex] = {
        ...fields[fieldIndex],
        type: value,
      };
      sections[sectionIndex] = {
        ...sections[sectionIndex],
        fields,
      };
      return {
        ...prevData,
        sections,
      };
    });
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Create Item</DialogTitle>
      <DialogContent>
        <TextField
          margin="dense"
          label="Title"
          type="text"
          fullWidth
          value={editedData.title}
          onChange={(e) => handleInputChange('title', e.target.value)}
        />
        <Select
          value={editedData.category}
          onChange={(e) => handleCategoryChange(e.target.value)}
          style={{ marginTop: '10px', width: '100%' }}
        >
          {catigories.map((category, index) => (
            <MenuItem key={index} value={category}>
              {category}
            </MenuItem>
          ))}
        </Select>

        <TextField
          margin="dense"
          label="Notes"
          type="text"
          fullWidth
          value={editedData.notes}
          onChange={(e) => handleInputChange('notes', e.target.value)}
        />
        <div style={{ marginTop: '10px' }}>
          <Typography variant="subtitle1">Tags</Typography>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {editedData.tags && editedData.tags.map((tag, tagIndex) => (
              <div key={tagIndex} style={{ marginLeft: '20px', marginTop: '10px' }}>
                <TextField
                  margin="dense"
                  label={`Tag ${tagIndex + 1}`}
                  type="text"
                  fullWidth
                  value={tag}
                  onChange={(e) => handleTagChange(tagIndex, e.target.value)}
                />
                <IconButton onClick={() => handleDeleteTag(tagIndex)}>
                  <DeleteIcon />
                </IconButton>
              </div>
            ))}
            <Button onClick={handleAddTag}>Add Tag</Button>
          </div>
        </div>
        {editedData.sections &&
          editedData.sections.map((section, sectionIndex) => (
            <div key={sectionIndex} style={{ marginTop: '10px' }}>
              <TextField
                margin="dense"
                label={`Section ${sectionIndex + 1}`}
                type="text"
                fullWidth
                value={section.section}
                onChange={(e) => handleSectionNameChange(sectionIndex, e.target.value)}
                disabled={section.section === 'INIT'}
              />
              <IconButton onClick={() => handleDeleteSection(sectionIndex)} disabled={section.section === 'INIT'}>
                <DeleteIcon />
              </IconButton>
              {section.fields.map((field, fieldIndex) => (
                <div key={fieldIndex} style={{ marginLeft: '20px', marginTop: '10px' }}>
                  <TextField
                    margin="dense"
                    label={`Field ${fieldIndex + 1} Label`}
                    type="text"
                    fullWidth
                    value={field.label}
                    onChange={(e) => handleFieldChange(sectionIndex, fieldIndex, 'label', e.target.value)}
                  />
                  <TextField
                    margin="dense"
                    label={`Field ${fieldIndex + 1} Value`}
                    type="text"
                    fullWidth
                    value={field.value}
                    onChange={(e) => handleFieldChange(sectionIndex, fieldIndex, 'value', e.target.value)}
                  />
                  <Select
                    value={field.type}
                    onChange={(e) => handleTypeChange(sectionIndex, fieldIndex, e.target.value)}
                    style={{ marginTop: '10px' }}
                  >
                    {types.map((type, index) => (
                      <MenuItem key={index} value={type}>
                        {type}
                      </MenuItem>
                    ))}
                  </Select>
                  <IconButton onClick={() => handleDeleteField(sectionIndex, fieldIndex)}>
                    <DeleteIcon />
                  </IconButton>
                </div>
              ))}
              <Button onClick={() => handleAddField(sectionIndex)}>Add Field</Button>
            </div>
          ))}
        <Button onClick={handleAddSection}>Add Section</Button>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleSaveClick} color="primary">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const SafeDetails = ({ data, safe, password, private_key, local_key, onUploadSafe, uploadProgress, token, dataState }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [selectedItemForEdit, setSelectedItemForEdit] = useState(null);
  const [configurationCatigories, setConfigurationCatigories] = useState([]);
  const [configurationTypes, setConfigurationTypes] = useState([]);
  
  const handleEditClick = (item) => {
    setSelectedItemForEdit(item);
    setIsEditing(true);
  };

  const handleEditSave = (editedData) => {
    setIsEditing(false);
  };
  const safeFiles = data.files.find((file) => file.safe_id === safe.id);

  // Calculate disk space utilization percentage
  const filledPercentage = (data.disk.filled_space / data.disk.total_space) * 100;

  const [decryptedDescription, setDecryptedDescription] = useState('');

  useEffect(() => {
    const decryptData = async () => {
      try {
        const decryptPrivateKey:any = await CryptoHelper.decrypt(private_key, get_device_hash(), Buffer.from(local_key, 'utf-8'));
        const decryptPassword:any = await CryptoHelper.decrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));
        const decryptedDesc:any = await CryptoHelper.decrypt(safe.description, decryptPassword, decryptPrivateKey);
        setDecryptedDescription(decryptedDesc);
        let apiSettings: any = new APISettings()
        let settings = await apiSettings.response
        setConfigurationCatigories(settings&& settings.data.item_categories)
        setConfigurationTypes(settings&& settings.data.item_types)
      } catch (error) {
        console.error('Error decrypting data:', error);
      }
    };
    decryptData();
  }, [safe.description, password, private_key, local_key]);

  return (
    <Paper elevation={3} style={{ padding: '16px', marginBottom: '16px', overflow: 'auto' }}>
      <Typography variant="h5" style={{ overflow: 'auto', whiteSpace: 'nowrap' }}>
        Name: {safe.name}
        <Typography
        variant="body1"
      >
        Description: {decryptedDescription}
      </Typography>
      </Typography>
      <Typography variant="body2">Items Count: {safe.count_items}</Typography>
      <Tooltip title="Create item"><IconButton onClick={handleEditClick}><AddIcon/></IconButton></Tooltip>
        {isEditing && (
            <EditModalItem
              password={password}
              local_key={local_key}
              private_key={private_key}
              dataState={dataState}
              catigories={configurationCatigories}
              types={configurationTypes}
              open={isEditing}
              onClose={() => setIsEditing(false)}
              onSave={handleEditSave}
              data={selectedItemForEdit}
              token={token}
              safe_id={safe.id}
          />
      )}
      <Tooltip title="Upload Files">
        {uploadProgress > 0 ? (
          <CircularProgress
            variant="indeterminate" // Change from "determinate" to "indeterminate"
            color="primary"
            sx={{ width: '100%' }}
          />
        ) : (
          <IconButton>
            <div>
              <label>
                <FileUploadIcon />
                <input onChange={(e) => onUploadSafe(safe.id, e.target.files)} type="file" style={{ display: 'none' }} multiple />
              </label>
            </div>
          </IconButton>
        )}
      </Tooltip>


      <Typography variant="h6" style={{ marginTop: '16px' }}>
        Disk Information
      </Typography>

      {/* Wrap LinearProgress with ThemeProvider */}
      <ThemeProvider theme={theme(getUtilizationColor(filledPercentage))}>
        <Box mt={2}>
          <LinearProgress
            variant="determinate"
            value={filledPercentage}
            color="primary" // Use 'primary' to apply the custom color from your theme
            sx={{ borderRadius: '5px', height: '10px', backgroundColor: '#f1f1f1' }}
          />
        </Box>
      </ThemeProvider>

      {/* Display percentage and a colored bar indicating the utilization */}
      <Box
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginTop: '8px',
        }}
      >
        <Typography>{`${filledPercentage.toFixed(2)}% Utilized`}</Typography>
        <Typography
          sx={{
            marginLeft: '8px',
          }}
        >
          {formatBytes(data.disk.filled_space)} / {formatBytes(data.disk.total_space)}
        </Typography>
      </Box>
    </Paper>
  );
};



// Helper function to format bytes into GB
const formatBytes = (bytes) => {
  const gigabytes = bytes / (1024 ** 3);
  return `${gigabytes.toFixed(2)} GB`;
};

// Helper function to determine color based on utilization percentage
const getUtilizationColor = (percentage) => {
  if (percentage < 50) {
    return '#00FF00';
  } else if (percentage < 80) {
    return '#FFA500';
  } else {
    return '#FF0000';
  };
};

const ItemList = ({ items, onSelectItem }) => (
  <ScrollableContainer maxHeight="300px">
    <List>
      {items.map((itemGroup) => (
        <div key={itemGroup.safe_id}>
          <Typography variant="h6" style={{ marginBottom: '8px' }}>
            Items
          </Typography>
          {itemGroup.items && itemGroup.items.length > 0 && itemGroup.items.map((item) => (
            <ListItem button key={item.id} onClick={() => onSelectItem(item)}>
              <ListItemText primary={item.title} secondary={`Category: ${item.category}`} />
              {item.favorite ? (
                    <StarIcon />
                ) : (
                    <StarBorderPurple500SharpIcon />
                )}
            </ListItem>
          ))}
          <Divider />
        </div>
      ))}
    </List>
  </ScrollableContainer>
);

function bytesToMB(bytes) {
  const megabytes = bytes / (1024 * 1024);
  return megabytes.toFixed(2);
}

const FilesList = ({ files, onSelectFile }) => (
  <ScrollableContainer maxHeight="250px">
    <List>
      {files.map((fileGroup) => (
        <div key={fileGroup.safe_id}>
          <Typography variant="h6" style={{ marginBottom: '8px' }}>
            Files
          </Typography>
          {fileGroup.objects.map((item) => (
            <ListItem button key={item.id} onClick={() => onSelectFile(item)}>
              <ListItemText
                primary={item.name}
                secondary={`Size: ${bytesToMB(item.size)} MB | Updated At: ${new Date(item.updated_at * 1000).toLocaleString()}`}
              />
            </ListItem>
          ))}
          <Divider />
        </div>
      ))}
    </List>
  </ScrollableContainer>
);

const FileDetails = ({ token, selectedSafe, selectedFile, handleDelete }) => {
  const handleDownload = async () => {
    try {
      const api = new APIFileDownload(token);
      await api.execute(selectedFile);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };
  
  return (
    <Paper elevation={3} style={{ padding: '16px', marginTop: '0px', marginLeft: '43px', width: '100%', overflow: 'auto' }}>
      {selectedFile && JSON.stringify(selectedFile).length !== 0 && (
        <div key={selectedFile.id}>
          <Typography variant="body1">File Name: {selectedFile.name}</Typography>
          <Typography variant="body1">Updated At: {new Date(selectedFile.updated_at * 1000).toLocaleString()}</Typography>
          <Typography variant="body1">Size: {bytesToMB(selectedFile.size)} MB</Typography>
          <Button onClick={handleDownload}>Download</Button><Button onClick={() => handleDelete(selectedSafe.id, selectedFile.id)} color="error">Delete</Button>
          <Divider />
        </div>
      )}
    </Paper>
  );
};


const ItemDetails = ({ dataState, token, selectedItem, selectedsafe, safes, handleDeleteItem, setStar, password, local_key, private_key }) => {
  const decryptPrivateKey = CryptoHelper.decrypt(private_key, get_device_hash(), Buffer.from(local_key, 'utf-8'));
  const decryptPassword = CryptoHelper.decrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));

  const [selectedSafe, setSelectedSafe] = useState('');
  const [anchorEl, setAnchorEl] = useState(null);

  const handleSafeClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleSafeClose = () => {
    setAnchorEl(null);
  };

  const handleSafeSelect = async (safe) => {
    setSelectedSafe(safe);
    let api = new APIMoveItem(token)
    await api.execute(selectedsafe.id, safe.id, selectedItem.id)
    const updatedData = await new APIGetAllItems(token).execute();
    dataState(updatedData.data);
    handleSafeClose();
  };

  return(
      <>
        <style jsx global>{`
          /* Global styles for custom scrollbar */
          div.scrollbar-container {
            scrollbar-width: thin;
            scrollbar-color: #1976D2 #f1f1f1;
          }

          div.scrollbar-container::-webkit-scrollbar {
            width: 10px;
          }

          div.scrollbar-container::-webkit-scrollbar-thumb {
            background-color: #1976D2;
            border-radius: 5px;
          }

          div.scrollbar-container::-webkit-scrollbar-track {
            background-color: #f1f1f1;
          }
        `}</style>
      <Paper elevation={3} className="scrollbar-container" style={{ padding: '20px', margin: '20px', width: '100%', maxWidth: '100%', maxHeight: '50vh', overflow: 'auto', border: '2px solid #ddd', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' }}>
        {selectedItem && JSON.stringify(selectedItem).length !== 0 && (
          <div key={selectedItem.id}>
            <Typography variant="h5" style={{ marginBottom: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                {selectedItem.title}
                {selectedItem.favorite ? (
                  <IconButton onClick={setStar}>
                    <StarIcon />
                  </IconButton>
                ) : (
                  <IconButton onClick={setStar}>
                    <StarBorderPurple500SharpIcon />
                  </IconButton>
                )}
              </div>
              <Tooltip title="Relocate">
                <IconButton onClick={handleSafeClick}>
                  <ArrowBackIcon />
                </IconButton>
              </Tooltip>
              <IconButton onClick={handleDeleteItem}>
                <DeleteOutlineOutlinedIcon />
              </IconButton>
            </Typography>
            {renderDetail("ID", selectedItem.id)}
            {renderDetail("Category", selectedItem.category)}
            {selectedItem.sections &&
              selectedItem.sections.map((section) => (
                <div key={section.section} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '10px', marginBottom: '10px', overflow: 'auto' }}>
                  <Typography variant="subtitle1">{section.section}</Typography>
                  <List>
                    {section.fields.map((field, index) => (
                      <ListItem key={index}>
                        <ListItemText primary={`${field.label}: ${CryptoHelper.decrypt(field.value, decryptPassword, Buffer.from(decryptPrivateKey, 'utf-8'))}`} />
                      </ListItem>
                    ))}
                  </List>
                </div>
              ))}
            {renderDetail("Tags", selectedItem.tags && selectedItem.tags.length > 0 ? selectedItem.tags.join(', ') : 'No tags')}
            {renderDetail("Notes", CryptoHelper.decrypt(selectedItem.notes, decryptPassword, Buffer.from(decryptPrivateKey, 'utf-8')))}
            <Divider />
          </div>
        )}
      </Paper>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleSafeClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
      >
        {safes.map((safe, index) => (
          <MenuItem key={index} onClick={() => handleSafeSelect(safe)}>
            {safe.name}
          </MenuItem>
        ))}
      </Menu>
    </>
  )
  
  function renderDetail(label, value) {
    return (
      <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '10px', marginBottom: '10px', overflow: 'auto' }}>
        <Typography variant="body1">{label}: {value}</Typography>
      </div>
    );
  }
};

export default function Home() {
  const [token, setToken] = useState('');
  const [local_key, setLocalKey] = useState('');
  const [password, setPassword] = useState('');
  const [private_key, setPrivateKey] = useState('');
  const [data, setData] = useState(null);
  const [selectedSafe, setSelectedSafe] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [open, setOpen] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false); // New state for loading
  const [editModalOpen, setEditModalOpen] = useState(false);

  // New state variables for the edited data
  const [editedName, setEditedName] = useState('');
  const [editedDescription, setEditedDescription] = useState('');

  const [uploadProgress, setUploadProgress] = useState(0);


  const router = useRouter();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const secureDataString = localStorage.getItem('secure');

        if (secureDataString !== null) {
          let secureData = JSON.parse(secureDataString);
          const currentToken = secureData ? secureData.token : '400';
          setToken(currentToken);
          const api = new APIGetAllItems(currentToken);
          const response = await api.execute();
          setLocalKey(secureData.local_key);
          setPassword(secureData.password);
          setPrivateKey(secureData.private_key);
          setData(response.data);
        } else {
          console.error('secureDataString is null');
          // Redirect to the login page or another page for authentication
          router.push('/auth/signin'); // Adjust the URL as needed
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        // Redirect to an error page or another appropriate page
        router.push('/auth/signin'); // Adjust the URL as needed
      }
    };

    fetchData();
  }, [router]); // Include router in the dependency array

  const handleEditClick = (safe) => {
    setEditedName(safe.name);
    setEditedDescription(safe.description);
    setEditModalOpen(true);
  };

  // Function to close the edit modal
  const handleEditClose = () => {
    setEditModalOpen(false);
  };

  const handleSelectSafe = (safe) => {
    setSelectedSafe(safe);
    setSelectedItem(null);
    setSelectedFile(null);
  };

  const handleSelectItem = (item) => {
    setSelectedItem(item);
    setSelectedFile(null);
  };

  const handleSelectFile = (file) => {
    setSelectedFile(file);
    setSelectedItem(null);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };
  
  const handleClose = () => {
    setOpen(false);
  };
  
  const handleEditSave = useCallback(async (name, description) => {
    try {
      setLoading(true); // Set loading to true to disable buttons

      const decrypt_private_key:any = CryptoHelper.decrypt(private_key, get_device_hash(), Buffer.from(local_key, 'utf-8'));
      const decrypt_password:any = CryptoHelper.decrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));

      let safe_id: any = selectedSafe&&selectedSafe.id

      await new APISafeUpdate(token, name, description).execute(safe_id)
      const updatedData = await new APIGetAllItems(token).execute();

      setData(updatedData.data);
      setEditModalOpen(false);
      setEditedName('');
      setEditedDescription('');
    } catch (error) {
      console.error('Error updating safe:', error);
      setEditedName('');
      setEditedDescription('');
    } finally {
      setLoading(false); // Set loading to false to enable buttons after request completes
      setEditedName('');
      setEditedDescription('');
    }
  }, [token, selectedSafe&&selectedSafe.id, editedName, editedDescription]);

  const handleSave = useCallback(async () => {
    try {
      setLoading(true); // Set loading to true to disable buttons

      const decrypt_private_key:any = CryptoHelper.decrypt(private_key, get_device_hash(), Buffer.from(local_key, 'utf-8'));
      const decrypt_password:any = CryptoHelper.decrypt(password, get_device_hash(), Buffer.from(local_key, 'utf-8'));

      const encrypt_description = CryptoHelper.encrypt(description, decrypt_password, decrypt_private_key);

      console.log('encrypt_description', encrypt_description);

      const apiSafeCreate = new APISafeCreate(token, name, encrypt_description);
      const newSafe = await apiSafeCreate.execute();

      // Fetch updated data after creating a new safe
      const updatedData = await new APIGetAllItems(token).execute();

      setData(updatedData.data);
      setOpen(false);
      setName('');
      setDescription('');
    } catch (error) {
      console.error('Error creating safe:', error);
      setName('');
      setDescription('');
    } finally {
      setLoading(false); // Set loading to false to enable buttons after request completes
      setName('');
      setDescription('');
    }
  }, [token, name, description, private_key, local_key, password]);

  const handleUploadFiles = async (safe_id, files) => {
    try {
      const uploadResults = [];
  
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
  
        const api = new APIFileUpload(token);
  
        await api.execute(safe_id, file, {
          onUploadProgress: (progressEvent) => {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(progress);
          },
        });
  
        uploadResults.push(file.name);
      }
  
      // Reset upload progress after completion
      setUploadProgress(0);
  
      const updatedData = await new APIGetAllItems(token).execute();
      setData(updatedData.data);
    } catch (error) {
      console.error('Error uploading files:', error);
      setUploadProgress(0);
    } finally {
      // Perform any cleanup or additional actions if needed
    }
  };
  
  const handleDeleteFile = async (safe_id, file_id)=>{
    try{
      const api = new APIFileDelete(token);
      await api.execute(safe_id, file_id);
      const updatedData = await new APIGetAllItems(token).execute();
      setData(updatedData.data);
    } catch (error){
      console.error('Error deleting safe:', error);
    }
    finally{
      
    }
  }

  const handleSafedelete = async (safe_id: string) =>{
    try{
      const apiSafeDelete = new APISafeDelete(token);
      await apiSafeDelete.execute(safe_id);
      const updatedData = await new APIGetAllItems(token).execute();
      setData(updatedData.data);
    } catch (error){
      console.error('Error deleting safe:', error);
    }
  }

  const handleSetFavorite = async () => {
    try{
      let api = new APIFavorite(token)
      let safe: any = selectedSafe&&selectedSafe.id
      let item: any = selectedItem&&selectedItem.id
      await api.execute(safe, item)
      const updatedData = await new APIGetAllItems(token).execute();
      setData(updatedData.data);
    } catch (error){
      console.error('Error: ', error);
    }
  }

  const handleDeleteItem= async () => {
    try{
      let api = new APIDeleteItem(token)
      let safe: any = selectedSafe&&selectedSafe.id
      let item: any = selectedItem&&selectedItem.id
      await api.execute(safe, item)
      const updatedData = await new APIGetAllItems(token).execute();
      setData(updatedData.data);
    } catch (error){
      console.error('Error: ', error);
    }
  }

  if (!data) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </div>
    );
  }

  return (
    <>
      <NavBar />
      <Container style={{ display: 'flex', flexDirection: 'row', marginTop: '20px', marginLeft: 0 }}>
        <div style={{ flex: 1, maxWidth: '25%' }}>
        <IconButton onClick={handleClickOpen}><AddIcon/></IconButton>
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>Add Safe</DialogTitle>
            <DialogContent>
              <TextField
                autoFocus
                margin="dense"
                label="Name"
                type="text"
                fullWidth
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              <TextField
                margin="dense"
                label="Description"
                type="text"
                fullWidth
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClose} color="primary" disabled={loading}>
                Cancel
              </Button>
              <Button onClick={handleSave} color="primary" disabled={loading}>
                Save
              </Button>
            </DialogActions>
          </Dialog>
          <SafeList
            safes={data.safes}
            onDeleteSafe={handleSafedelete}
            onSelectSafe={handleSelectSafe}
            handleEditClick={handleEditClick} // Add this line
          />
          <EditModal
            open={editModalOpen}
            onClose={handleEditClose}
            onSave={handleEditSave}
            name={editedName}
            description={editedDescription}
            loading={loading}
            setName={setEditedName}
            setDescription={setEditedDescription}
            password={password}
            private_key={private_key}
            local_key={local_key}
          />
        </div>
        <div style={{ flex: 1, maxWidth: '25%' }}>
          {selectedSafe && <SafeDetails dataState={setData} token={token} uploadProgress={uploadProgress} onUploadSafe={handleUploadFiles} local_key={local_key} password={password} private_key={private_key} data={data} safe={selectedSafe} />}
          {selectedSafe && (
            <ItemList
              items={data.list.filter((item) => item.safe_id === selectedSafe.id)}
              onSelectItem={handleSelectItem}
            />
          )}

          {selectedSafe && (
            <FilesList
              files={data.files.filter((fileGroup) => fileGroup.safe_id === selectedSafe.id)}
              onSelectFile={handleSelectFile}
            />
          )}

        </div>
        <div style={{ flex: 1 ,maxWidth: '50%' }}>
          {selectedItem && <ItemDetails password={password} local_key={local_key} private_key={private_key} dataState={setData} token={token} selectedsafe={selectedSafe} safes={data.safes} handleDeleteItem={handleDeleteItem} setStar={handleSetFavorite} selectedItem={selectedItem} />}
          {selectedFile && <FileDetails selectedSafe={selectedSafe} handleDelete={handleDeleteFile} token={token} selectedFile={selectedFile} />}
        </div>
      </Container>
    </>
  );
}