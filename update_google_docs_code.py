from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

SCOPES = ["https://www.googleapis.com/auth/documents"]

def get_service():
    load_dotenv("credentials/.env")
    credentials_path = os.getenv("GOOGLE_DOCS_CREDENTIALS_PATH")
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    return build("docs", "v1", credentials=credentials)

def clear_document(service, doc_id):
    """Clear all content from the Google Doc."""
    try:
        # Get the current document
        doc = service.documents().get(documentId=doc_id).execute()
        
        # Get the length of the content
        content_length = doc.get('body').get('content', [])[-1].get('endIndex', 1)
        
        if content_length > 1:  # Only clear if there's content
            requests = [{
                'deleteContentRange': {
                    'range': {
                        'startIndex': 1,  # Start from 1 to preserve the required first paragraph
                        'endIndex': content_length - 1
                    }
                }
            }]
            
            service.documents().batchUpdate(
                documentId=doc_id, body={"requests": requests}
            ).execute()
            print("Successfully cleared document")
    except Exception as e:
        print(f"Error clearing document: {str(e)}")

def insert_code_blocks(doc_id, file_paths):
    service = get_service()
    
    # Clear the document first
    clear_document(service, doc_id)
    
    # Get the fresh document state after clearing
    doc = service.documents().get(documentId=doc_id).execute()
    end_index = doc.get('body').get('content', [])[-1].get('endIndex', 1)
    
    requests = []
    current_index = end_index - 1
    
    for path in file_paths:
        try:
            with open(path, "r") as file:
                code = file.read()
            
            path_length = len(path)
            code_length = len(code)
            
            requests.extend([
                {
                    "insertText": {
                        "location": {"index": current_index},
                        "text": f"\n{path}\n"
                    }
                },
                {
                    "updateParagraphStyle": {
                        "range": {
                            "startIndex": current_index,
                            "endIndex": current_index + path_length + 2
                        },
                        "paragraphStyle": {"namedStyleType": "HEADING_2"},
                        "fields": "namedStyleType"
                    }
                },
                {
                    "insertText": {
                        "location": {"index": current_index + path_length + 2},
                        "text": f"{code}\n"
                    }
                },
                {
                    "updateTextStyle": {
                        "range": {
                            "startIndex": current_index + path_length + 2,
                            "endIndex": current_index + path_length + code_length + 3
                        },
                        "textStyle": {
                            "weightedFontFamily": {"fontFamily": "Roboto Mono"},
                            "backgroundColor": {
                                "color": {"rgbColor": {"red": 0.95, "green": 0.95, "blue": 0.95}}
                            }
                        },
                        "fields": "weightedFontFamily,backgroundColor"
                    }
                }
            ])
            
            current_index += path_length + code_length + 3
            
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")
    
    try:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()
        print("Successfully added code blocks to document")
    except Exception as e:
        print(f"Error updating document: {str(e)}")

if __name__ == "__main__":
    doc_id = "1-nhehVT8Y1kGM1k7bard33fMwNvOEytO3Tz8WiVvDCE"
    paths = [
        "backend/app/main.py",
        "backend/app/models.py",
        "frontend-apps/web-app/src/App.js",
        "frontend-apps/web-app/src/index.js",
        "frontend-apps/web-app/src/hooks/useWebSocket.js",
        "frontend-apps/web-app/src/config/api.js",
        "frontend-apps/web-app/src/components/LoginForm.js",
        "frontend-apps/web-app/src/components/MainApp.js",
        "frontend-apps/web-app/src/components/Settings.js",
        "frontend-apps/web-app/src/components/TaskList.js",
        "frontend-apps/web-app/src/components/Timer.js",
        "frontend-apps/web-app/src/styles/theme.css"


    ]
    
    insert_code_blocks(doc_id, paths)