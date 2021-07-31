from terminal_game import directory, root_dir, file


class Parser(object):
    @staticmethod
    def parse_root(root_dr_contents):
        dr = root_dir.RootDir([])

        for content in root_dr_contents:
            content.update({'parent': dr})
            if isinstance(content['contents'], list):
                dr.add(Parser.parse_dir(content))
            else:
                dr.add(Parser.parse_file(content))

        return dr

    @staticmethod
    def parse_dir(dr_dict):
        dr = directory.Directory(dr_dict['name'], [], dr_dict['parent'])

        for content in dr_dict['contents']:
            content.update({'parent': dr})
            if isinstance(content['contents'], list):
                dr.add(Parser.parse_dir(content))
            else:
                dr.add(Parser.parse_file(content))

        return dr

    @staticmethod
    def parse_file(fl_dict):
        return file.File(fl_dict['name'], fl_dict['contents'], fl_dict['parent'])