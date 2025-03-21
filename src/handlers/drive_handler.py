# Handles Google Drive file operations
import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import io
import tempfile

# Set up logging
logger = logging.getLogger(__name__)

class DriveHandler:
    """
    Handles Google Drive file operations.
    """
    
    def __init__(self, credentials_path=None):
        """
        Initializes the DriveHandler with Google Drive API credentials.
        
        Args:
            credentials_path: Path to the service account credentials JSON file
        """
        self.credentials_path = credentials_path or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        self.service = None
        
        if not self.credentials_path:
            logger.error("Google Drive credentials path not provided")
            raise ValueError("Google Drive credentials path not provided")
        
        self._authenticate()
    
    def _authenticate(self):
        """
        Authenticates with the Google Drive API using service account credentials.
        """
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, 
                scopes=['https://www.googleapis.com/auth/drive']
            )
            self.service = build('drive', 'v3', credentials=credentials)
            logger.info("Successfully authenticated with Google Drive API")
        except Exception as e:
            logger.error(f"Error authenticating with Google Drive API: {e}")
            raise
    
    def find_folder(self, folder_path):
        """
        Finds a folder in Google Drive by path.
        
        Args:
            folder_path: Path to the folder (e.g., "Computers/G4V0JD34/USV/My Calendar/My Daily Notes")
            
        Returns:
            str: Folder ID if found, None otherwise
        """
        # Split the path into components
        path_components = folder_path.strip('/').split('/')
        
        # Start from the root of My Drive
        parent_id = 'root'
        
        # Traverse the path
        for component in path_components:
            query = f"name = '{component}' and '{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            
            try:
                results = self.service.files().list(
                    q=query,
                    spaces='drive',
                    fields='files(id, name)'
                ).execute()
                
                items = results.get('files', [])
                
                if not items:
                    logger.warning(f"Folder '{component}' not found in path '{folder_path}'")
                    return None
                
                # Use the first matching folder
                parent_id = items[0]['id']
            except Exception as e:
                logger.error(f"Error finding folder '{component}': {e}")
                return None
        
        return parent_id
    
    def create_folder(self, folder_name, parent_id='root'):
        """
        Creates a folder in Google Drive.
        
        Args:
            folder_name: Name of the folder to create
            parent_id: ID of the parent folder
            
        Returns:
            str: Folder ID if created successfully, None otherwise
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            logger.info(f"Created folder '{folder_name}' with ID: {folder.get('id')}")
            return folder.get('id')
        except Exception as e:
            logger.error(f"Error creating folder '{folder_name}': {e}")
            return None
    
    def ensure_folder_path(self, folder_path):
        """
        Ensures that a folder path exists in Google Drive, creating folders as needed.
        
        Args:
            folder_path: Path to the folder (e.g., "Computers/G4V0JD34/USV/My Calendar/My Daily Notes")
            
        Returns:
            str: ID of the final folder in the path
        """
        # Split the path into components
        path_components = folder_path.strip('/').split('/')
        
        # Start from the root of My Drive
        parent_id = 'root'
        
        # Traverse the path, creating folders as needed
        for component in path_components:
            query = f"name = '{component}' and '{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            
            try:
                results = self.service.files().list(
                    q=query,
                    spaces='drive',
                    fields='files(id, name)'
                ).execute()
                
                items = results.get('files', [])
                
                if not items:
                    # Folder doesn't exist, create it
                    parent_id = self.create_folder(component, parent_id)
                    if not parent_id:
                        logger.error(f"Failed to create folder '{component}' in path '{folder_path}'")
                        return None
                else:
                    # Use the existing folder
                    parent_id = items[0]['id']
            except Exception as e:
                logger.error(f"Error ensuring folder '{component}': {e}")
                return None
        
        return parent_id
    
    def find_file(self, file_name, parent_folder_id):
        """
        Finds a file in a Google Drive folder.
        
        Args:
            file_name: Name of the file to find
            parent_folder_id: ID of the parent folder
            
        Returns:
            dict: File metadata if found, None otherwise
        """
        try:
            query = f"name = '{file_name}' and '{parent_folder_id}' in parents and trashed = false"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, modifiedTime)'
            ).execute()
            
            items = results.get('files', [])
            
            if not items:
                logger.info(f"File '{file_name}' not found in folder '{parent_folder_id}'")
                return None
            
            # Return the first matching file
            logger.info(f"Found file '{file_name}' with ID: {items[0]['id']}")
            return items[0]
        except Exception as e:
            logger.error(f"Error finding file '{file_name}': {e}")
            return None
    
    def create_file(self, file_name, content, parent_folder_id, mime_type='text/markdown'):
        """
        Creates a file in Google Drive.
        
        Args:
            file_name: Name of the file to create
            content: Content of the file
            parent_folder_id: ID of the parent folder
            mime_type: MIME type of the file
            
        Returns:
            str: File ID if created successfully, None otherwise
        """
        try:
            # Create a temporary file with UTF-8 encoding
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.md') as temp_file:
                # Replace emoji characters that might cause encoding issues
                sanitized_content = self._sanitize_content(content)
                temp_file.write(sanitized_content)
                temp_file_path = temp_file.name
            
            # Upload the file to Google Drive
            file_metadata = {
                'name': file_name,
                'parents': [parent_folder_id]
            }
            
            media = MediaFileUpload(
                temp_file_path,
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            logger.info(f"Created file '{file_name}' with ID: {file.get('id')}")
            return file.get('id')
        except Exception as e:
            logger.error(f"Error creating file '{file_name}': {e}")
            return None
    
    def _sanitize_content(self, content):
        """
        Sanitizes content to avoid encoding issues.
        
        Args:
            content: Content to sanitize
            
        Returns:
            str: Sanitized content
        """
        # Replace common emoji characters with text equivalents
        emoji_replacements = {
            '💭': '[thinking]',  # thinking bubble
            '💪': '[strength]',  # strength
            '🚧': '[obstacle]',  # obstacle
            '✅': '[done]',      # checkmark
            '🙏': '[gratitude]', # gratitude
            '📚': '[content]'    # books/content
        }
        
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        return content
    
    def update_file(self, file_id, content, mime_type='text/markdown'):
        """
        Updates a file in Google Drive.
        
        Args:
            file_id: ID of the file to update
            content: New content of the file
            mime_type: MIME type of the file
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            # Create a temporary file with UTF-8 encoding
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.md') as temp_file:
                # Replace emoji characters that might cause encoding issues
                sanitized_content = self._sanitize_content(content)
                temp_file.write(sanitized_content)
                temp_file_path = temp_file.name
            
            # Update the file in Google Drive
            media = MediaFileUpload(
                temp_file_path,
                mimetype=mime_type,
                resumable=True
            )
            
            self.service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            logger.info(f"Updated file with ID: {file_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating file with ID '{file_id}': {e}")
            return False
    
    def read_file(self, file_id):
        """
        Reads a file from Google Drive.
        
        Args:
            file_id: ID of the file to read
            
        Returns:
            str: File content if read successfully, None otherwise
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file_content.seek(0)
            content = file_content.read().decode('utf-8')
            
            logger.info(f"Read file with ID: {file_id}")
            return content
        except Exception as e:
            logger.error(f"Error reading file with ID '{file_id}': {e}")
            return None
    
    def create_or_update_daily_note(self, date_str, content, folder_path):
        """
        Creates or updates a daily note in Google Drive.
        
        Args:
            date_str: Date string for the note (e.g., "2025-03-16")
            content: Content of the note
            folder_path: Path to the folder (e.g., "Computers/G4V0JD34/USV/My Calendar/My Daily Notes")
            
        Returns:
            tuple: (bool, str) - (Success status, File ID or error message)
        """
        try:
            # Ensure the folder path exists
            folder_id = self.ensure_folder_path(folder_path)
            if not folder_id:
                return False, "Failed to ensure folder path"
            
            # Check if the file already exists
            file_name = f"{date_str}.md"
            existing_file = self.find_file(file_name, folder_id)
            
            if existing_file:
                # Update the existing file
                success = self.update_file(existing_file['id'], content)
                if success:
                    return True, existing_file['id']
                else:
                    return False, "Failed to update file"
            else:
                # Create a new file
                file_id = self.create_file(file_name, content, folder_id)
                if file_id:
                    return True, file_id
                else:
                    return False, "Failed to create file"
        except Exception as e:
            logger.error(f"Error creating or updating daily note: {e}")
            return False, str(e)
