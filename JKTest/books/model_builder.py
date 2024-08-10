import ast
import joblib
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split


class ModelBuilder:
    """
    Model Builder based on datasets
    """
    def __init__(self):
        self.file_path = '../datasets/books.csv'
        self.books = None
        self.celaned_books = None
        self.all_genres = set()
        self.features_scaled = None
        self.knn = None
        self.scaler = StandardScaler()


    def data_collector(self):
        """
        Data collection
        """
        try:
            self.books = pd.read_csv(self.file_path, on_bad_lines='skip')
        except pd.errors.ParserError:
            print("ParserError: Trying to read the file with a different delimiter or encoding.")
            # Attempt with a different delimiter
            try:
                self.books = pd.read_csv(self.file_path, sep=',')  # Adjust the delimiter if needed
            except pd.errors.ParserError:
                # Attempt with a different encoding
                try:
                    self.books = pd.read_csv(self.file_path, encoding='ISO-8859-1')  # Adjust the encoding if needed
                except pd.errors.ParserError as e:
                    print(f"Failed to parse CSV file: {e}")
        return self.books
    
    def convert_to_list(self, genre_str):
        """
        Convert genre strings to lists
        """
        try:
            return ast.literal_eval(genre_str)
        except (ValueError, SyntaxError):
            return []


    def data_cleanup(self):
        """
        Data Cleanup and update missing data
        """
        # Select relevant columns
        self.books = self.books[['title', 'author', 'rating', 'genres']]

        # Check for null values in each column
        null_values = self.books.isnull().sum()
        print("Null values in each column:")
        print(null_values)

        # # Fill missing values in 'rating' with the mean
        # self.books['rating'].fillna(self.books['rating'].mean(), inplace=True)

        # # Fill missing values in 'genres' with 'Unknown'
        # self.books['genres'].fillna('Unknown', inplace=True)

        # Convert genre strings to lists
        self.books['genre_list'] = self.books['genres'].apply(self.convert_to_list)

        # Extract unique genres
        for genres in self.books['genre_list']:
            self.all_genres.update(genres)

    
    def feature_fit_transoform(self):
        # Fit MultiLabelBinarizer with all unique genres
        self.mlb = MultiLabelBinarizer(classes=sorted(self.all_genres))
        genre_encoded = self.mlb.fit_transform(self.books['genre_list'])

        # Create a DataFrame for the encoded genres
        genre_df = pd.DataFrame(genre_encoded, columns=self.mlb.classes_)

        # Combine the encoded genres with the original DataFrame
        self.books = self.books.join(genre_df)

        # Select relevant features
        # Adjust columns to drop as needed
        self.features = self.books.drop(columns=['genres', 'genre_list', 'title', 'author'])
        # Standardize the features
        self.features_scaled = self.scaler.fit_transform(self.features)


    def data_trainer(self):
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.features_scaled, self.books, test_size=0.3, random_state=42)
        # Prepare features and target
        # X = self.books.drop(columns=['book_id', 'title', 'authors', 'genres'])
        # y = self.books['rating']
        # Train the model
        # self.knn = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(X)
        # Train the k-NN model
        self.knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
        self.knn.fit(X_train)  
    
    def build_model(self):
        joblib.dump(self.knn, '../models/book_recommendation_model.pkl')

    # Function to recommend books
    def recommend_books(self, genres, rating, n_recommendations=5):
        genres_list = self.convert_to_list(genres)
        if not all(genre in self.mlb.classes_ for genre in genres_list):
            raise ValueError("One or more genres not found in the training data.")
        genre_encoded_input = self.mlb.transform([genres_list])
        
        # Create a DataFrame with the same structure as features
        input_data = pd.DataFrame(genre_encoded_input, columns=self.mlb.classes_)
        input_data['rating'] = rating
        
        # Reorder columns to match the scaler's training data
        input_data = input_data[self.features.columns]

        # Standardize the input data
        input_scaled = self.scaler.transform(input_data)
        model = joblib.load('../models/book_recommendation_model.pkl')

        # Find similar books
        distances, indices = model.kneighbors(input_scaled)
        # distances, indices = model.kneighbors(input_scaled, n_neighbors=n_recommendations)
        recommended_books = self.books.iloc[indices[0]]
        return recommended_books


if __name__ == "__main__":
    obj = ModelBuilder()
    # Collect Data
    obj.data_collector()
    # Data Cleanup
    obj.data_cleanup()
    # Feature selection
    obj.feature_fit_transoform()
    # Data Trainer
    obj.data_trainer()
    # Build Model
    obj.build_model()
    # Model Test 
    try:
        recommended_books = obj.recommend_books("['Buddhism']", 4.5)
        print("Recommended books based on genres 'Buddhism' and rating 4.5:")
        print(recommended_books[['title', 'genres', 'rating']])
    except ValueError as e:
        print(e) 

