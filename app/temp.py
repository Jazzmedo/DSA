import sqlite3
import os

def update_image_paths():
    conn = sqlite3.connect('content.db')
    c = conn.cursor()
    
    # Update image paths for the blog table
    c.execute('SELECT id, image1, image2, image3, image4 FROM blog')
    blog_rows = c.fetchall()
    for row in blog_rows:
        id, *images = row
        updated_images = [img.replace('\\', '/') if img else None for img in images]
        c.execute('''
            UPDATE blog
            SET image1 = ?, image2 = ?, image3 = ?, image4 = ?
            WHERE id = ?
        ''', (*updated_images, id))
    
    # Update image paths for the news table
    c.execute('SELECT id, image1, image2, image3, image4 FROM news')
    news_rows = c.fetchall()
    for row in news_rows:
        id, *images = row
        updated_images = [img.replace('\\', '/') if img else None for img in images]
        c.execute('''
            UPDATE news
            SET image1 = ?, image2 = ?, image3 = ?, image4 = ?
            WHERE id = ?
        ''', (*updated_images, id))
    
    conn.commit()
    conn.close()

# Call the function to update the image paths
update_image_paths()
